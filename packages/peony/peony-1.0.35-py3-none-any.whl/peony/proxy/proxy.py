
import signal
import os
# linux 默认就是epoll
from twisted.internet import reactor

from .connection.client_tcp_connection import ClientConnectionFactory as ClientTCPConnectionFactory
from .connection.client_udp_connection import ClientConnectionFactory as ClientUDPConnectionFactory
from .connection.admin_connection import AdminConnectionFactory
from .stat_counter import StatCounter
from ..share import constants
from ..share.log import logger
from ..share.utils import safe_call


class Proxy(object):
    """
    proxy相关
    """

    client_tcp_connection_factory_class = ClientTCPConnectionFactory
    client_udp_connection_factory_class = ClientUDPConnectionFactory

    admin_connection_factory_class = AdminConnectionFactory

    app = None

    # 统计
    stat_counter = None

    def __init__(self, app):
        """
        构造函数
        :return:
        """
        self.app = app
        self.stat_counter = StatCounter()

    def run(self):
        # 启动对外监听
        host_list = self.app.host
        if isinstance(host_list, str):
            # 说明是字符串，要转化成数组
            host_list = (host_list,)

        if self.app.config['TCP']:
            for host in host_list:
                reactor.listenTCP(self.app.port, self.client_tcp_connection_factory_class(self),
                                  backlog=self.app.backlog, interface=host)

        if self.app.config['UDP']:
            for host in host_list:
                reactor.listenUDP(
                    self.app.port, self.client_udp_connection_factory_class(self),
                    interface=host
                )

        # 启动admin服务
        admin_address = self.app.config['ADMIN_ADDRESS']

        if admin_address:
            if isinstance(admin_address, (list, tuple)):
                # 说明是网络协议
                reactor.listenTCP(admin_address[1], self.admin_connection_factory_class(self),
                                  interface=admin_address[0])
            elif isinstance(admin_address, str):
                # 说明是文件
                if os.path.exists(admin_address):
                    os.remove(admin_address)

                # 创建目录
                admin_directory = os.path.dirname(admin_address)
                if admin_directory and not os.path.exists(admin_directory):
                    os.makedirs(admin_directory)

                reactor.listenUNIX(admin_address, self.admin_connection_factory_class(self))
            else:
                logger.error('invalid admin address. proxy: %s, admin_address: %s', self, admin_address)

        try:
            reactor.run(installSignalHandlers=False)
        except:
            logger.error('exc occur. proxy: %s', self, exc_info=True)

    def stop(self):
        """
        停止
        :return:
        """
        try:
            # 直接调用stop是关闭不了的
            reactor.callFromThread(reactor.stop)
        except:
            logger.error('exc occur.', exc_info=True)

    def __repr__(self):
        return '<%s name: %s>' % (
            type(self).__name__, self.app.name
        )
