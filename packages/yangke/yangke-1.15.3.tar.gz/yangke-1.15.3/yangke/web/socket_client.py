#!/usr/bin/python3
# 文件名：client.py

# 导入 socket、sys 模块
import socket
import sys
import time

from yangke.base import stop_threads, execute_function_by_interval, start_threads
from yangke.common.config import logger
from yangke.nlp.chatgpt import chat


def deal(msg: str):
    print(f"客户端回调处理消息{msg}!")


def deal_http(msg: str):
    msg: dict = eval(msg)
    action = msg.get('Action')
    if action == "ChatGPT":
        question = msg.get("Question")
        res = chat(question)
        msg.update({"Res": res})
    return msg


class ClientSocket:
    def __init__(self, host="localhost", port=9990, callback=None):
        """

        Parameters
        ----------
        host
        port
        callback: 当socket接收到数据时的回调函数，如果该回调函数不返回信息，则数据只是在本地进行处理，如果返回数据，则ClientSocket会将返回的信息发送给websocket端口，返回的数据类型必须是str
        """
        self.host = socket.gethostname() if host == "localhost" else host
        self.port = port
        self.callback = callback
        # 创建 socket 对象
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_client(self, damon=False):
        """
        开启socket通信连接，并开始监听端口，处理服务器发送的消息

        Parameters
        ----------
        damon
        是否开启守护线程，监听并阻塞当前进程，如果为True，则该进程永远不会退出，如果为False，则在新线程中监听socket端口的消息

        Returns
        -------

        """

        # 连接服务，指定主机和端口
        self.socket.connect((self.host, self.port))
        if damon:
            self.msg_received()
        else:
            start_threads(self.msg_received)  # 开启新进程处理接收到的服务器信息

    def msg_received(self):
        while True:
            # 接收小于 1024 字节的数据
            msg = self.socket.recv(1024)
            msg = msg.decode('utf8')
            if msg.startswith('connect done'):
                logger.info(f"已建立与websocket服务端的连接，发送数据准备就绪！")
            else:
                if self.callback is None:
                    self.callback = deal
                # noinspection all
                res = self.callback(msg)
                if res is None:
                    pass
                elif isinstance(res, dict) and len(res) == 0:
                    pass
                else:
                    self.send(res)

    def send(self, msg):
        msg = str(msg).encode('utf8')
        self.socket.send(msg)


if __name__ == "__main__":
    client = ClientSocket(callback=deal_http, port=9990, host='182.43.65.44')
    client.start_client(damon=True)
    # i = 0
    # while True:
    #     i += 1
    #     time.sleep(1)
    #     client.send(i)
