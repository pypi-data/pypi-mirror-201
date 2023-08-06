from flask import Flask, request, make_response
import hashlib
import xml.etree.ElementTree as ET
from yangke.common.config import logger, add_file_logger
from yangke.web.flaskserver import start_server_app


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


def chat_with_gpt(text):
    # 调用ChatGPT的API接口，返回对话结果
    logger.debug("调用ChatGPT的API接口，返回对话结果")
    return "调用ChatGPT的API接口，返回对话结果"


def generate_text_response(xml_tree, content):
    # 根据对话结果生成XML格式的回复消息
    logger.debug("根据对话结果生成XML格式的回复消息")
    return "根据对话结果生成XML格式的回复消息"


def forward_to_ipv6_machine():
    """
    将接收到的ipv4请求转发给ipv6机器
    Returns
    -------

    """


def connect_with_ipv6_machine():
    """
    与ipv6机器l
    Returns
    -------

    """


if __name__ == "__main__":
    add_file_logger('log.txt')
    host = "0.0.0.0"
    port = 10080
    logger.debug(f"服务已启动{host}:{port}")
    # app.run(host='0.0.0.0', port=10080)
    start_server_app(deal=chat_with_gpt, host=host, port=port)
