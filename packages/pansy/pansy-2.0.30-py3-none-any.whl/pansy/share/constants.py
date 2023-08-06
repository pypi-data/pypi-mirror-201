NAME = 'pansy'

CMD_CLIENT_REQ              = 10  # 透传client请求
CMD_CLIENT_CLOSED           = 20  # 客户端连接被关闭

CMD_WRITE_TO_WORKER         = 100 # 给worker发送消息

CMD_WORKER_ASK_FOR_TASK     = 210 # 请求任务

CMD_WRITE_TO_USERS          = 230 # 主动下发
CMD_CLOSE_USERS             = 250 # 关闭多个客户端

CMD_WRITE_TO_MEMBERS        = 300 # 发送给房间内所有成员
CMD_CLOSE_MEMBERS           = 310 # 关闭房间所有成员的连接


DEFAULT_CONFIG = dict(
    HOST='127.0.0.1',
    PORT=9700,

    # 启动的room id 列表，闭区间
    ROOM_ID_BEGIN=None,
    ROOM_ID_END=None,
    # 同时并发房间数
    ROOM_CONCURRENT=1,

    DEBUG=False,

    BOX_CLASS='netkit.box.Box',

    # master class
    MASTER_CLASS='pansy.master.Master',

    # station class
    STATION_CLASS='pansy.station.Station',

    # worker class
    WORKER_CLASS='pansy.worker.Worker',

    NAME=NAME,

    CONN_TIMEOUT=None,

    # 重连等待时间。worker和client都在用
    RECONNECT_INTERVAL=1,

    STOP_TIMEOUT=None,

    # 处理task超时(秒). 超过后会打印fatal日志. None 代表永不超时
    WORK_TIMEOUT=None,

    # 等待处理的tasks的最大值。<=0代表无限
    TASKS_MAX_SIZE=-1,
)
