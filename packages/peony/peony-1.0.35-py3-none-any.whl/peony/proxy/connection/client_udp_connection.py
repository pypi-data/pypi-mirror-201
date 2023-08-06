
from twisted.internet.protocol import DatagramProtocol

from ...share.utils import safe_call
from ...share.log import logger
from ...share import constants


class ClientConnectionFactory(DatagramProtocol):

    def __init__(self, proxy):
        self.proxy = proxy

    def datagramReceived(self, data, address):
        # address: type: tuple, format: ('127.0.0.1', 62043)

        while data:
            task = self.proxy.app.task_class()
            ret = task.unpack(data)

            if ret == 0:
                # 说明要继续收
                logger.error('buffer incomplete. proxy: %s, ret: %d, read_buffer: %r',
                             self.proxy, ret, data)
                return
            elif ret > 0:
                # 收好了
                # 不能使用双下划线，会导致别的地方取的时候变为 _Gateway__raw_data，很奇怪
                task._raw_data = data[:ret]
                data = data[ret:]
                safe_call(self._on_read_complete, task, address)
                continue
            else:
                # 数据已经混乱了，全部丢弃
                logger.error('buffer invalid. proxy: %s, ret: %d, read_buffer: %r',
                             self.proxy, ret, data)
                data = b''
                return

    def _on_read_complete(self, task, address):
        self.proxy.stat_counter.client_req += 1

        group_id = self.proxy.app.group_router(task)
        self.proxy.stat_counter.add_worker_req(group_id)
        # 直接发送到对应的group_id
        if not self.proxy.app.master.push_task(group_id, task):
            self.proxy.stat_counter.add_discard_task(group_id)
