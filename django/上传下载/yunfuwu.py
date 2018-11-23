# yunfuwu.py
from socket import *
import os,sys
import signal
import time

#文件库路径
FILE_PATH = "/home/tarena/mydata/"
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)

#将文件服务器功能写在类中：
class FtpSever(object):
    # """docstring for FtpSever"""
    def __init__(self, connfd):
        self.connfd = connfd
    
    def do_list(self):
        #获取文件列表
        file_list = os.listdir(FILE_PATH)
        if not file_list:
            self.connfd.send('文件库为空'.encode())
            return
        else:
            self.connfd.send(b"ok")
            time.sleep(0.1)

        files = ''
        for file in file_list:
            if file[0] != '.' and \
            os.path.isfile(FILE_PATH + file):
                files = files + file + '#'
        self.connfd.sendall(files.encode())
    def  do_get(self,filename):
        try:
            fd = open(FILE_PATH + filename,'rb')
        except:
            self.connfd.send("文件不存在".encode())
            return
        self.connfd.send(b'ok')
        time.sleep(0.1)
        #发送文件
        while True:
            data = fd.read(1024)
            if not data:
                time.sleep(0.1)#防止"**"与之前文件粘连
                self.connfd.send(b'**')
                break
            self.connfd.send(data)
        print("文件已发送")

    def do_put(self,filename):
        try:
            fd = open(FILE_PATH + filename,'wb')#先打开接收到的文件

        except:
            self.connfd.send("上传失败".encode)#有错误的话，反馈一个信息
        self.connfd.send(b'ok')
        while True:
            data = self.connfd.recv(1024)
            if data == b'$':#收到信号时，结束
                break
            fd.write(data)#写入文件
        fd.close()#写好之后．关闭
        print('上传完成')

#创建套接字，接收客户端连接，创建新的进程
def main():
    # pass
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sockfd.bind(ADDR)
    sockfd.listen(5)

    #处理子进程退出
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    print("Listen the port 8000 ...")

    while True:
        try:
            connfd,addr = sockfd.accept()
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit("服务器退出")
        except Exception as e:
            print("服务器异常：",e)
            continue

        print("已连接客户端：",addr)
        #创建子进程
        pid = os.fork()
        if pid == 0:
            sockfd.close()
            ftp = FtpSever(connfd)
            # print("执行客户端请求")
            # sys.exit()
            #判断客户端请求
            while True:
                data = connfd.recv(1024).decode()
                if not data or data[0] == 'Q':
                    connfd.close()
                    sys.exit("客户端退出")
                elif data[0] == 'L':
                    print("LLLL")
                    ftp.do_list()
                elif data[0] == 'G':
                    filename = data.split(' ')[-1]
                    ftp.do_get(filename)
                elif data[0] == 'P':
                    filename = data.split(" ")[-1]
                    ftp.do_put(filename)
        else:
            connfd.close()
            continue

if __name__ == "__main__":
    main()





