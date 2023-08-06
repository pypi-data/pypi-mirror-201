import os
import queue
import signal
import time
from pyglet.clock import Clock
import _thread
import setproctitle
from maple import constants as maple_constants

from ..share import constants
from ..share.log import logger
from ..share.utils import safe_call


class Worker:
    app = None
    group_id = None

    enabled = True

    # 业务可以通过clock来设置schedule
    clock = None

    _got_first_request = False

    # pipe 比 queue性能高一点，因为queue是在pipe的基础上加了锁
    # 但是最终还是得选择queue，因为pipe.recv是阻塞的，也就是每次poll完了只能读取一次
    # 这会导致clock的计算次数增加，没必要
    _task_queue = None

    # 工作进展
    _work_progress = None

    def __init__(self, app, group_id, task_queue):
        self.app = app
        self.group_id = group_id
        self._task_queue = task_queue

        self.clock = self._create_clock()

    def run(self):
        setproctitle.setproctitle(self.app.make_proc_name(
            'worker:%s' % self.group_id
        ))

        self._handle_signals()

        self._on_start()

        # daemon==True，主线程不需要等待网络线程结束
        _thread.start_new_thread(self._monitor_work_timeout, ())

        while self.enabled:
            try:
                self._handle()
            except:
                logger.error('exc occur. worker: %s', self, exc_info=True)

        self._on_stop()

    def _create_clock(self):
        """
        创建clock
        """
        return Clock()

    def _handle(self):
        """
        主循环，等待网络消息，并进行处理
        """
        # 允许idle
        sleep_time = self.clock.get_sleep_time(True)
        # sleep_time is None 说明没有需要处理的，直接永久阻塞等待即可
        # 否则就要使用指定时间阻塞等待
        task_list = []

        # 第一个get要block
        block = True
        # 已经领取的task的数量，单独一个变量是为了性能考虑
        task_claimed_count = 0

        while self.enabled and not (
                task_claimed_count >= self.app.task_claimed_max_size > 0
        ):
            try:
                task_list.append(
                    self._task_queue.get(block=block, timeout=sleep_time)
                )

                task_claimed_count += 1
            except queue.Empty:
                # 说明已经没有了
                break
            except OSError:
                # 当term信号处理函数调用了queue.close()
                # 会在这里抛出异常 handle is closed
                # 直接break就好
                break
            except:
                # 说明出问题了
                logger.error('exc occur. worker: %s', self, exc_info=True)
                break
            finally:
                block = False

        self.app.events.activate_worker(self)
        for bp in self.app.blueprints:
            bp.events.app_activate_worker(self)

        for task in task_list:
            request = self.app.request_class(self, task)
            # 设置task开始处理的时间和信息
            self._work_progress = dict(
                begin_time=time.perf_counter(),
                request=request,
            )

            self._handle_request(request)

            self._work_progress = None

        safe_call(self.clock.tick, True)

        for bp in self.app.blueprints:
            bp.events.app_deactivate_worker(self)
        self.app.events.deactivate_worker(self)

    def _handle_request(self, request):
        """
        出现任何异常的时候，服务器不再主动关闭连接
        """
        if not request.is_valid:
            return False

        if request.task.cmd not in (maple_constants.CMD_CLIENT_CREATED, maple_constants.CMD_CLIENT_CLOSED) \
                and not request.view_func:
            logger.info('cmd invalid. request: %s' % request)
            return False

        if not self._got_first_request:
            self._got_first_request = True
            self.app.events.before_first_request(request)
            for bp in self.app.blueprints:
                bp.events.before_app_first_request(request)

        self.app.events.before_request(request)
        for bp in self.app.blueprints:
            bp.events.before_app_request(request)
        if request.blueprint:
            request.blueprint.events.before_request(request)

        if request.interrupted:
            # 业务要求中断
            return True

        view_func_exc = None

        if request.task.cmd == maple_constants.CMD_CLIENT_CREATED:
            self.app.events.create_client(request)
            for bp in self.app.blueprints:
                bp.events.create_app_client(request)
        elif request.task.cmd == maple_constants.CMD_CLIENT_CLOSED:
            self.app.events.close_client(request)
            for bp in self.app.blueprints:
                bp.events.close_app_client(request)
        else:
            try:
                request.view_func(request)
            except Exception as e:
                logger.error('view_func raise exception. e: %s, request: %s', e, request, exc_info=True)
                view_func_exc = e

        if request.blueprint:
            request.blueprint.events.after_request(request, view_func_exc)
        for bp in self.app.blueprints:
            bp.events.after_app_request(request, view_func_exc)
        self.app.events.after_request(request, view_func_exc)

        return True

    def _monitor_work_timeout(self):
        """
        监控task的耗时
        :return:
        """

        while True:
            time.sleep(1)

            work_progress = self._work_progress
            if work_progress:
                past_time = time.perf_counter() - work_progress['begin_time']
                if self.app.work_timeout is not None and past_time > self.app.work_timeout:
                    # 说明worker的处理时间已经太长了
                    logger.fatal('work timeout: %s / %s, request: %s',
                                 past_time, self.app.work_timeout, work_progress['request'])
                    # 强制从子线程退出整个进程
                    os._exit(-1)

    def _on_start(self):
        """
        当worker启动后
        可继承实现
        :return:
        """
        self.app.events.start_worker(self)
        for bp in self.app.blueprints:
            bp.events.start_app_worker(self)

    def _on_stop(self):
        """
        当worker停止前
        可继承实现
        :return:
        """
        for bp in self.app.blueprints:
            bp.events.stop_app_worker(self)
        self.app.events.stop_worker(self)

    def _handle_signals(self):
        def safe_stop_handler(signum, frame):
            self.enabled = False
            # 如果队列处于get中的话，会直接打断并抛出异常 OSError: handle is closed
            # 经测试不会影响其他worker对于该队列的读取
            safe_call(self._task_queue.close)

        # 安全停止
        signal.signal(signal.SIGTERM, safe_stop_handler)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGHUP, signal.SIG_IGN)

    def __repr__(self):
        return '<%s name: %s, group_id: %r>' % (
            type(self).__name__, self.app.name, self.group_id
        )

