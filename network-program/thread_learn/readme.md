线程创建的两种方式
    simple_thread_1.py
        t1 = threading.Thread(target=run, args=('t1',)) 创建
        t1.start()                                      启动
    simple_thread_2.py
        类方式，见代码

join
    等待线程运行完成
    t.join()

setDaemon
    设置线程为守护线程
    非守护线程：未设置为守护线程的线程
    非守护线程结束，守护线程自动结束
    设置位置必须在线程启动（start）之前
    t.setDaemon(True)
    t.start()

lock
    线程锁
    作用：保证共享资源数据的安全性
    lock = threading.Lock()    设置
    lock.acquire()              获取锁
    lock.release()              释放锁

Rlock
    递归锁
    lock = threading.RLock()    设置
    lock.acquire()              获取锁
    lock.release()              释放锁

semaphore
    信息量
    semaphore = threading.BoundedSemaphore(5)   设置了最多信号量
    semaphore.acquire()                         获取
    semaphore.release()                         释放

event事件
    event = threading.Event()       创建
    event.set()                 设置状态
    event.isSet()               判定状态
    event.clear()               清空状态
    event.is_set()              判定状态，与event.isSet()相同
    event.wait()                等待设置状态，阻塞模式

队列queue
    作用：
        （1）解耦
        （2）提高效率
    队列是有顺序的容器。
    列表与队列的不同之处：
        队列是数据仅一份，取走就没有了。数据存放在内存中。
        列表是数据的拷贝，除非手动删除数据，数据一直存在。

    q = queue.Queue()       先输入先出 FIFO
    q.put(xxx)              存放数据
    q.get()                 仅能顺序取数据，无数据时，会阻塞
    q.get(block=False)      仅能顺序取数据，无数据时，报错，不阻塞
    q.get(timeout=1)        仅能顺序取数据，无数据时，等待超时时间，报错，不阻塞
    q.qsize()               查看队列数据长度
    q.get_nowait()          仅能顺序取数据，无数据时，报错，不阻塞
    q = queue.Queue(maxsize=3)
    q.put(xxx)              最多放3个，多了就阻塞

    q = queue.LifoQueue()   后进先出 LIFO
    q = queue.PriorityQueue()   具有优先级的队列，数字越小，优先级越高
    q.put((2, 'second'))
    q.put((-1, 'first'))
    q.put((9, 'third'))
