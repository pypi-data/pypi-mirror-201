
"""
封装通过group_id来访问数据的功能
"""

import multiprocessing
import queue
from ..share.log import logger
from ..share.utils import safe_call


class TaskQueueManager(object):
    """
    通过group_id来区分的queue
    """

    max_size = None
    queue_dict = None

    def __init__(self, group_id_list, max_size=-1):
        self.max_size = max_size
        self.queue_dict = dict()
        for group_id in group_id_list:
            self.queue_dict[group_id] = multiprocessing.Queue(self.max_size)

    def get_queue(self, group_id):
        """
        获取对应的队列
        :param group_id:
        :return:
        """
        return self.queue_dict.get(group_id)

    def put(self, group_id, item):
        """
        加入item
        如果成功返回True，如果失败返回False
        :param group_id:
        :param item:
        :return:
        """
        try:
            self.queue_dict[group_id].put_nowait(item)
            return True
        except queue.Full:
            logger.error(
                'put item fail, queue is full. group_id: %s, max_size: %s',
                group_id, self.max_size
            )
            return False
        except:
            logger.error('put item fail, exc occur. group_id: %s', group_id, exc_info=True)
            return False

    def get(self, group_id):
        if self.empty(group_id):
            return None
        else:
            return self.queue_dict[group_id].get_nowait()

    def clear(self, group_id):
        """
        清空
        :param group_id:
        :return:
        """
        self.queue_dict.pop(group_id, None)

    def clear_all(self):
        """
        清空所有
        :return:
        """
        self.queue_dict.clear()

    def empty(self, group_id):
        """
        判断是否是空的
        :param group_id:
        :return:
        """
        return self.queue_dict[group_id].empty()

    def qsize(self, group_id):
        """
        某个队列的size
        :param group_id:
        :return:
        """
        return self.queue_dict[group_id].qsize()

    def close(self):
        """
        如果队列里面有数据的话结束不了进程
        :return:
        """

        for q in self.queue_dict.values():
            safe_call(q.close)
