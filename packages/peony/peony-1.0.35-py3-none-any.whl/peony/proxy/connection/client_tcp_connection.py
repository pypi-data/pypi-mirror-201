
from twisted.internet.protocol import Protocol, Factory, connectionDone
from twisted.internet import reactor

from ...share.utils import safe_call
from ...share.log import logger


class ClientConnectionFactory(Factory):

    def __init__(self, proxy):
        self.proxy = proxy

    def buildProtocol(self, addr):
        return ClientConnection(self, addr)


class ClientConnection(Protocol):
    _read_buffer = None

    # 过期timer
    _expire_timer = None

    def __init__(self, factory, address):
        # address: IPv4Address
        self.factory = factory
        self.address = address
        self._read_buffer = b''

    def connectionMade(self):
        self.transport.setTcpNoDelay(True)

        self.factory.proxy.stat_counter.clients += 1

        self._set_expire_callback()

    def connectionLost(self, reason=connectionDone):
        self._clear_expire_callback()

        self.factory.proxy.stat_counter.clients -= 1

    def dataReceived(self, data):
        """
        当数据接受到时
        :param data:
        :return:
        """
        self._read_buffer += data

        while self._read_buffer:
            # 因为task后面还是要用的
            task = self.factory.proxy.app.task_class()
            ret = task.unpack(self._read_buffer)
            if ret == 0:
                # 说明要继续收
                return
            elif ret > 0:
                # 收好了
                # 不能使用双下划线，会导致别的地方取的时候变为 _Gateway__raw_data，很奇怪
                task._raw_data = self._read_buffer[:ret]
                self._read_buffer = self._read_buffer[ret:]
                safe_call(self._on_read_complete, task)
                continue
            else:
                # 数据已经混乱了，全部丢弃
                logger.error('buffer invalid. proxy: %s, ret: %d, read_buffer: %r',
                             self.factory.proxy, ret, self._read_buffer)
                self._read_buffer = b''
                return

    def _on_read_complete(self, task):
        """
        完整数据接收完成
        :param task: 解析之后的task
        :return:
        """
        self.factory.proxy.stat_counter.client_req += 1
        self._set_expire_callback()

        group_id = self.factory.proxy.app.group_router(task)
        self.factory.proxy.stat_counter.add_worker_req(group_id)
        # 直接发送到对应的group_id
        if not self.factory.proxy.app.master.push_task(group_id, task):
            self.factory.proxy.stat_counter.add_discard_task(group_id)

    def _set_expire_callback(self):
        """
        注册超时之后的回调
        :return:
        """

        if self.factory.proxy.app.client_timeout is None:
            return

        self._clear_expire_callback()

        self._expire_timer = reactor.callLater(
            self.factory.proxy.app.client_timeout, self._expire_callback
        )

    def _clear_expire_callback(self):
        """
        清空超时之后的回调
        :return:
        """
        if self._expire_timer:
            self._expire_timer.cancel()
            self._expire_timer = None

    def _expire_callback(self):
        """
        能关闭的话，就关闭掉
        :return:
        """
        self._expire_timer = None

        if self.transport and self.transport.connected:
            self.transport.loseConnection()
