
import json

from twisted.internet.protocol import Protocol, Factory
from netkit.box import Box

from ...share.utils import safe_call
from ...share.log import logger
from ...share import constants


class AdminConnectionFactory(Factory):

    def __init__(self, proxy):
        self.proxy = proxy

    def buildProtocol(self, addr):
        return AdminConnection(self, addr)


class AdminConnection(Protocol):
    _read_buffer = None

    def __init__(self, factory, address):
        self.factory = factory
        self.address = address
        self._read_buffer = b''

    def dataReceived(self, data):
        """
        当数据接受到时
        :param data:
        :return:
        """
        self._read_buffer += data

        while self._read_buffer:
            # 因为box后面还是要用的
            box = Box()
            ret = box.unpack(self._read_buffer)
            if ret == 0:
                # 说明要继续收
                return
            elif ret > 0:
                # 收好了
                self._read_buffer = self._read_buffer[ret:]
                safe_call(self._on_read_complete, box)
                continue
            else:
                # 数据已经混乱了，全部丢弃
                logger.error('buffer invalid. proxy: %s, ret: %d, read_buffer: %r',
                             self.factory.proxy, ret, self._read_buffer)
                self._read_buffer = b''
                return

    def _auth_user(self, username, password):
        """
        验证用户
        :param username:
        :param password:
        :return:
        """

        return (self.factory.proxy.app.config['ADMIN_USERNAME'] or '',
                self.factory.proxy.app.config['ADMIN_PASSWORD'] or '') == (
            username or '', password or ''
        )

    def _on_read_complete(self, box):
        """
        完整数据接收完成
        :param box: 解析之后的box
        :return:
        """

        # 无论是哪一种请求，都先验证用户
        req_body = json.loads(box.body)

        rsp = None

        if not self._auth_user(req_body['auth']['username'], req_body['auth']['password']):
            rsp = box.map(dict(
                ret=constants.RET_ADMIN_AUTH_FAIL
            ))
        else:
            if box.cmd == constants.CMD_ADMIN_SERVER_STAT:
                workers = len(self.factory.proxy.app.master.worker_processes)
                # 正在处理的tasks
                try:
                    pending_tasks = dict([(group_id, queue.qsize()) for group_id, queue in
                                         self.factory.proxy.app.master.task_queue_manager.queue_dict.items()])
                except:
                    # mac下会报错qsize没有实现
                    logger.error('exc occur', exc_info=True)
                    pending_tasks = dict()

                rsp_body = dict(
                    clients=self.factory.proxy.stat_counter.clients,
                    workers=workers,
                    client_req=self.factory.proxy.stat_counter.client_req,
                    worker_req=self.factory.proxy.stat_counter.worker_req_counter,
                    pending_tasks=pending_tasks,
                    discard_tasks=self.factory.proxy.stat_counter.discard_tasks_counter,
                )

                rsp = box.map(dict(
                    body=json.dumps(rsp_body)
                ))

            elif box.cmd == constants.CMD_ADMIN_STOP:
                self.factory.proxy.app.master.stop_all()
                rsp = box.map(dict(
                    ret=0
                ))

        if rsp:
            self.transport.write(rsp.pack())

