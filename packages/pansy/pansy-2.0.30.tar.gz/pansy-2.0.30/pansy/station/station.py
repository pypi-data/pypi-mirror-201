import signal
import setproctitle
import threading


class Station:
    app = None
    room_id_begin = None
    room_id_end = None

    enabled = True

    worker_threads = None

    def __init__(self, app, room_id_begin, room_id_end):
        self.app = app
        self.room_id_begin = room_id_begin
        self.room_id_end = room_id_end
        self.worker_threads = list()

    def run(self):
        setproctitle.setproctitle(self.app.make_proc_name(
            'station:%s-%s' % (self.room_id_begin, self.room_id_end)
        ))
        self._handle_signals()

        self._spawn_worker_threads()

    def _create_worker_thread(self, room_id):
        worker = self.app.worker_class(self, room_id)

        thread = threading.Thread(
            target=worker.run,
        )
        # master不可以独自退出
        thread.daemon = False
        # 标记room_id
        thread.room_id = room_id
        # 用来给task_queue发数据
        thread.worker = worker

        thread.start()

        return thread

    def _spawn_worker_threads(self):
        """
        监控线程
        :return:
        """
        for room_id in range(self.room_id_begin, self.room_id_end+1):
            self.worker_threads.append(self._create_worker_thread(room_id))

        # 线程的重新启动好像会有很多问题，因为worker里面不止一个线程
        # 还是简单直接join，也不考虑拉起了
        # 让各个线程自己去保证enabled==True时不会退出
        for thread in self.worker_threads:
            try:
                thread.join()
            except:
                # 命令行CTRL-C的时候可能抛异常
                pass

    def _handle_signals(self):
        def safe_stop_handler(signum, frame):
            self.enabled = False
            for thread in self.worker_threads:
                if thread and thread.is_alive():
                    # 为了打断get
                    thread.worker.push_task(None)

        # 安全停止
        signal.signal(signal.SIGTERM, safe_stop_handler)
        signal.signal(signal.SIGHUP, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    def __repr__(self):
        return '<%s name: %s, room_id_range: [%r, %r]>' % (
            type(self).__name__, self.app.name, self.room_id_begin, self.room_id_end
        )

