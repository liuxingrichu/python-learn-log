�����̵�ѧϰ��¼��

��socketע��㡿
��1��socket.send����ʹ�ã����ܻᷢ��ճ��
��2��socket.send���ݲ��ɴ���
��3��socket.recv������ģʽ
��4����socket.recv��������ʱ���ҽ�������Ϊ�գ���ʾ�ͻ��˶Ͽ����ӡ�


��socketserver�������̡�
��1��First, you must create a request handler class by subclassing the
BaseRequestHandlerclass and overriding its handle() method;
this method will process incoming requests. ����
��2��Second, you must instantiate one of the server classes,
passing it the server��s address and the request handler class.
��3��Then call the handle_request() or serve_forever() method of the server
object to process one or many requests.
��4��Finally, call server_close() to close the socket.

���http://www.cnblogs.com/alex3714/articles/5830365.html


��ʱ�����̡�ʱ�䡢ʵ�ַ�ʽ������
2017.2.19	socketʵ��ssh         ��������������ݴ�������ַ�ʽʵ��ճ������
2017.2.19   socketʵ��get_file    �ļ����غ�MD5
2017.2.19   socketserver����ʹ��   ���û������������

