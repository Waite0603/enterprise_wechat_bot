from flask import Flask, request
from callback.WXBizMsgCrypt3 import WXBizMsgCrypt
from lxml import etree
import time

from configobj import ConfigObj
from receive.PassiveRecovery import PassiveRecovery

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
    print(xml_tree)

    from_user = xml_tree.find("FromUserName").text
    to_user = xml_tree.find("ToUserName").text
    msg_type = xml_tree.find("MsgType").text

    print(from_user)
    print(to_user)
    print(msg_type)

    # 消息被动回复
    if msg_type == 'text':
        content = xml_tree.find("Content").text
        print(content)
        reply_xml = PassiveRecovery(to_user, from_user, msg_type, msg_content=content).text()
    else:
        media_id = xml_tree.find("MediaId").text
        print(media_id)
        reply_xml = PassiveRecovery(to_user, from_user, msg_type, media_id=media_id).image()

    # 加密回复的 XML
    ret, sEncryptMsg = wxcpt.EncryptMsg(reply_xml, nonce, timestamp)
    if ret != 0:
        return 'ERR: EncryptMsg ret: ' + str(ret)

    return sEncryptMsg


if __name__ == '__main__':
    app.run(debug=debug_mode, port=8888)
