
https://www.cnblogs.com/alex3714/articles/5248247.html
编程模式
    单线程：效率
    多线程：线程安全
    事件驱动：
        应用场景：多任务、低耦合、存在阻塞



http://www.cnblogs.com/alex3714/articles/5876749.html
IO模式
    （1）阻塞 I/O（blocking IO）
        socket 默认状态
        数据准备阶段、数据拷贝阶段都阻塞

    （2）非阻塞 I/O（nonblocking IO）
        需手动设置
        数据准备阶段不阻塞、但数据拷贝阶段阻塞
        用户进程需要不断询问kernel的数据准备状态

    （3）I/O 多路复用（ IO multiplexing）
        可同时监控多个socket
        数据准备阶段、数据拷贝阶段都阻塞
        任何一个socket数据准备完成，kernel就会通知用户进程

    （4）信号驱动 I/O（ signal driven IO）
    （5）异步 I/O（asynchronous IO）
        注：linux下的asynchronous IO其实用得很少
        数据准备阶段、数据拷贝阶段都不阻塞
        数据从kernel拷贝到用户进程后，再通知用户read

    注：由于signal driven IO在实际中并不常用

select，poll，epoll
    IO多路复用的机制
    同步IO，即需要用户进程自己从kernel拷贝数据到自己进程

    select(rlist, wlist, xlist, timeout=None)
        分别是readfds、writefds和exceptfds
        优点：跨平台
        缺点：linux下，默认支持1024，可修改

    epoll
        Windows不支持

python3 asyncio是异步IO