
NAME = 'peony'

# 系统返回码
# admin用户验证失败
RET_ADMIN_AUTH_FAIL = -20000


# 管理员命令
# 获取运行状态统计
CMD_ADMIN_SERVER_STAT = 20000

# 停止整个server
CMD_ADMIN_STOP = 21003


DEFAULT_CONFIG = dict(
    HOST='127.0.0.1',
    PORT=9250,

    # 监听TCP
    TCP=True,

    # 监听UDP
    UDP=False,

    # 启动的group列表。group_id必须为数字
    GROUP_LIST=[dict(id=1, count=1)],

    # 通过task路由group_id
    GROUP_ROUTER=lambda task: 1,

    DEBUG=False,

    # box class
    BOX_CLASS='netkit.box.Box',

    # task class
    TASK_CLASS='maple.Task',

    # master class
    MASTER_CLASS='peony.master.Master',

    # proxy class
    PROXY_CLASS='peony.proxy.Proxy',

    # worker class
    WORKER_CLASS='peony.worker.Worker',

    # request class
    REQUEST_CLASS='peony.worker.Request',

    NAME=NAME,

    # 每个worker的消息队列的最大长度, <=0 代表无限
    TASK_QUEUE_MAX_SIZE=-1,

    # 一次性认领的任务数量最大值，<=0 代表无限
    TASK_CLAIMED_MAX_SIZE=-1,

    # backlog
    BACKLOG=256,

    # 客户端连接超时
    CLIENT_TIMEOUT=None,

    STOP_TIMEOUT=None,

    # 处理task超时(秒). 超过后会打印fatal日志. None 代表永不超时
    WORK_TIMEOUT=None,

    # 管理员，可以连接proxy获取数据
    # 管理员访问地址: 'admin.sock' or ('127.0.0.1', 9910)
    ADMIN_ADDRESS='admin.sock',
    ADMIN_USERNAME=None,
    ADMIN_PASSWORD=None,
)
