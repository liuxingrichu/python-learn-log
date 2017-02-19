网络编程的学习记录：

【socket注意点】
（1）socket.send连续使用，可能会发生粘包
（2）socket.send数据不可传空
（3）socket.recv是阻塞模式
（4）当socket.recv不在阻塞时，且接受数据为空，表示客户端断开链接。


【socketserver操作流程】
（1）First, you must create a request handler class by subclassing the
BaseRequestHandlerclass and overriding its handle() method;
this method will process incoming requests. 　　
（2）Second, you must instantiate one of the server classes,
passing it the server’s address and the request handler class.
（3）Then call the handle_request() or serve_forever() method of the server
object to process one or many requests.
（4）Finally, call server_close() to close the socket.

详见http://www.cnblogs.com/alex3714/articles/5830365.html


【时间历程】时间、实现方式、功能
2017.2.19	socket实现ssh         命令解析、大数据处理和三种方式实现粘包处理
2017.2.19   socket实现get_file    文件下载和MD5
2017.2.19   socketserver基本使用   多用户与服务器交互

