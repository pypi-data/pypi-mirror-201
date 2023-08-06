
import multiprocessing
import signal
import time
import threading
import _thread
import setproctitle
from .task_queue_manager import TaskQueueManager
from ..share.utils import safe_call
from ..share.log import logger


class Master:

    app = None

    proxy = None
    worker_processes = None

    enabled = True

    task_queue_manager = None

    def __init__(self, app):
        self.app = app
        self.worker_processes = list()
        self.task_queue_manager = TaskQueueManager(
            [group['id'] for group in self.app.group_list],
            self.app.task_queue_max_size
        )

    def run(self):
        setproctitle.setproctitle(self.app.make_proc_name('master'))
        self._handle_signals()

        self._spawn_workers()

        thread_list = [
            # 监视workers
            threading.Thread(target=self._monitor_workers),
            # proxy
            threading.Thread(target=self._run_proxy)
        ]

        for t in thread_list:
            # 不可以独自退出
            t.daemon = False
            t.start()

        for t in thread_list:
            t.join()

        # 如果队列里还有数据的话，是无法退出进程的，会在这里等待队列结束
        self.task_queue_manager.close()

    def _run_proxy(self):
        self.proxy = self.app.proxy_class(self.app)
        self.proxy.run()

    def push_task(self, group_id, task):
        """
        指定worker的task
        :param group_id:
        :param task:
        :return:
        """

        return self.task_queue_manager.put(group_id, task)

    def _create_worker(self, group_id, task_queue):
        process = multiprocessing.Process(
            target=self.app.worker_class(self.app, group_id, task_queue).run,
        )
        # master不可以独自退出
        process.daemon = False
        process.init_params = dict(
            group_id=group_id,
            task_queue=task_queue
        )

        process.start()

        return process

    def _spawn_workers(self):
        """
        监控进程
        :return:
        """
        for group in self.app.group_list:
            group_id = group['id']
            for it in range(group['count']):
                self.worker_processes.append(self._create_worker(
                    group_id,
                    self.task_queue_manager.get_queue(group_id),
                ))

    def _monitor_workers(self):
        while True:
            for idx, process in enumerate(self.worker_processes):
                if process and not process.is_alive():
                    self.worker_processes[idx] = None

                    if self.enabled:
                        # 需要重启启动process
                        self.worker_processes[idx] = self._create_worker(**process.init_params)

            if not self.enabled and not any(self.worker_processes):
                # 可以彻底停掉了
                break

            time.sleep(0.1)

    def stop_all(self):
        """
        等所有子进程结束，父进程也退出
        """

        def kill_processes_later(processes, timeout):
            """
            等待一段时间后杀死所有进程
            :param processes:
            :param timeout:
            :return:
            """

            def _kill_processes():
                # 等待一段时间
                time.sleep(timeout)

                for p in processes:
                    if p and p.is_alive():
                        # 说明进程还活着
                        p.kill()

            _thread.start_new_thread(_kill_processes, ())

        self.enabled = False

        # 一定要这样，否则后面kill的时候可能会kill错
        processes = self.worker_processes[:]

        # 如果是终端直接CTRL-C，子进程自然会在父进程之后收到INT信号，不需要再写代码发送
        # 如果直接kill -INT $parent_pid，子进程不会自动收到INT
        # 所以这里可能会导致重复发送的问题，重复发送会导致一些子进程异常，所以在子进程内部有做重复处理判断。
        for p in processes:
            if p:
                p.terminate()

        if self.app.stop_timeout is not None:
            kill_processes_later(processes, self.app.stop_timeout)

        # 关闭proxy
        self.proxy.stop()

    def _handle_signals(self):

        def stop_handler(signum, frame):
            """
            等所有子进程结束，父进程也退出
            """
            self.stop_all()

        # TERM/INT 均为安全结束
        signal.signal(signal.SIGINT, stop_handler)
        signal.signal(signal.SIGTERM, stop_handler)
        signal.signal(signal.SIGHUP, signal.SIG_IGN)

    def __repr__(self):
        return '<%s name: %s>' % (
            type(self).__name__, self.app.name
        )
