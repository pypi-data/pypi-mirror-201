from flask import Flask, request, make_response
import hashlib
import xml.etree.ElementTree as ET
from yangke.common.config import logger, add_file_logger
from yangke.web.flaskserver import start_server_app
from yangke.web.socket_server import socket_communication_server

global socket


# app = Flask(__name__)


# @app.route('/', methods=['GET', 'POST'])
# def wechat_auth():
#     logger.debug(f"receive request")
#     if request.method == 'GET':
#         logger.debug("接收到GET请求")
#         token = '5d9d54c798119aab5dfc126ea45432a2'  # 替换为自己在公众号设置中的Token
#         data = request.args
#         signature = data.get('signature', '')
#         timestamp = data.get('timestamp', '')
#         nonce = data.get('nonce', '')
#         echostr = data.get('echostr', '')
#         list = [token, timestamp, nonce]
#         list.sort()
#         s = ''.join(list).encode('utf-8')
#         if (hashlib.sha1(s).hexdigest() == signature):
#             return make_response(echostr)
#         else:
#             return 'Invalid Signature'
#     else:
#         logger.debug("接收到POST请求")
#         xml_data = request.stream.read()
#         xml_tree = ET.fromstring(xml_data)
#         msg_type = xml_tree.find('MsgType').text
#         if msg_type == 'text':
#             content = xml_tree.find('Content').text
#             response_content = chat_with_gpt(content)
#             response = generate_text_response(xml_tree, response_content)
#             return make_response(response)
#         else:
#             response_content = '暂不支持该类型消息的回复。'
#             response = generate_text_response(xml_tree, response_content)
#             return make_response(response)

def on_receive_msg(msg):
    """
    接收到服务器的消息时，执行该方法

    Parameters
    ----------
    msg

    Returns
    -------

    """
    logger.debug(f"接收到客户端的消息：{msg}")


def deal(text: dict):
    """
    将请求参数发送给远程服务器，由远程服务器处理，本机只做数据转发
    Parameters
    ----------
    text

    Returns
    -------

    """
    if socket is not None:
        res = socket.get_answer_of_send(text)
        return res
    return {"error": "未知结果"}


def http_transfer_server(http_listen_port=80, transfer_listen_port=9990):
    """
    http请求转发方法，默认将请求到本机80端口的数据转发给远程服务器9990端口，无需指定远程服务器ip，但需要本机具有公网ipv4地址，远程服务器和
    http请求发送者都会通过本机ipv4地址建立连接

    Parameters
    ----------
    http_listen_port: 接受http请求的端口号
    transfer_listen_port: websocket转发请求信息的端口号，本端口与另一台真正提供服务的服务器通信

    Returns
    -------

    """
    global socket
    socket = socket_communication_server(call_back=on_receive_msg, port=transfer_listen_port)
    logger.debug(f"http服务已启动0.0.0.0:{http_listen_port}")
    start_server_app(deal=deal, host="0.0.0.0", port=http_listen_port, use_action=False)


if __name__ == "__main__":
    add_file_logger('log.txt')
    http_transfer_server(http_listen_port=80)
    # 测试url: http://localhost:80/?Action=ChatGPT&Question=核电站给水流量孔板的精度是多少？
