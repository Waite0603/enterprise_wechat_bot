from flask import Flask, request
from callback.WXBizMsgCrypt3 import WXBizMsgCrypt
from lxml import etree
import time

from configobj import ConfigObj

config = ConfigObj('./config.ini', encoding='utf-8')
debug_mode = config['dev'].as_bool('debug')

app = Flask(__name__)


@app.route('/', methods=['GET'])
def receive_callback():
    # 获取参数
    msg_signature = request.args.get('msg_signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')

    # 创建 WXBizMsgCrypt 对象
    wxcpt = WXBizMsgCrypt(config['wechat']['Token'], config['wechat']['EncodingAESKey'], config['wechat']['CorpID'])

    ret, sEchoStr = wxcpt.VerifyURL(msg_signature, timestamp, nonce, echostr)
    if ret != 0:
        return 'ERR: VerifyURL ret: ' + str(ret)

    return sEchoStr


@app.route('/', methods=['POST'])
def callback_message():
    # 获取参数
    msg_signature = request.args.get('msg_signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')

    # 获取 POST 的原始数据
    sReqData = request.data

    # 创建 WXBizMsgCrypt 对象
    wxcpt = WXBizMsgCrypt(config['wechat']['Token'], config['wechat']['EncodingAESKey'], config['wechat']['CorpID'])

    ret, sMsg = wxcpt.DecryptMsg(sReqData, msg_signature, timestamp, nonce)
    if ret != 0:
        return 'ERR: DecryptMsg ret: ' + str(ret)

    # 解析 XML
    xml_tree = etree.fromstring(sMsg)
    content = xml_tree.find("Content").text
    from_user = xml_tree.find("FromUserName").text
    to_user = xml_tree.find("ToUserName").text

    # print(content)
    # print(from_user)
    # print(to_user)

    # 构造回复的 XML
    reply_xml = """
    <xml>
        <ToUserName><![CDATA[{to_user}]]></ToUserName>
        <FromUserName><![CDATA[{from_user}]]></FromUserName>
        <CreateTime>{create_time}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{content}]]></Content>
    </xml>
    """.format(to_user=from_user, from_user=to_user, create_time=int(time.time()), content=content)

    # 加密回复的 XML
    ret, sEncryptMsg = wxcpt.EncryptMsg(reply_xml, nonce, timestamp)
    if ret != 0:
        return 'ERR: EncryptMsg ret: ' + str(ret)

    return sEncryptMsg


if __name__ == '__main__':
    app.run(debug=debug_mode)
