# coding = utf-8
import time


class PassiveRecovery(object):
    # 传入数据 to_user, from_user, msg_type, msg_content, media_id
    def __init__(self, to_user, from_user, msg_type, msg_content=None, media_id=None):
        self.to_user = to_user
        self.from_user = from_user
        self.msg_type = msg_type
        self.msg_content = msg_content
        self.media_id = media_id

    def text(self):
        return f"""<xml>
        <ToUserName><![CDATA[{self.to_user}]]></ToUserName>
        <FromUserName><![CDATA[{self.from_user}]]></FromUserName>
        <CreateTime>{int(time.time())}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{self.msg_content}]]></Content>
        </xml>"""

    def image(self):
        return f"""<xml>
        <ToUserName><![CDATA[{self.to_user}]]></ToUserName>
        <FromUserName><![CDATA[{self.from_user}]]></FromUserName>
        <CreateTime>{int(time.time())}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
            <MediaId><![CDATA[{self.media_id}]]></MediaId>
        </Image>
        </xml>"""

    def video(self):
        return f"""<xml>
        <ToUserName><![CDATA[{self.to_user}]]></ToUserName>
        <FromUserName><![CDATA[{self.from_user}]]></FromUserName>
        <CreateTime>{int(time.time())}</CreateTime>
        <MsgType><![CDATA[video]]></MsgType>
        <Video>
            <MediaId><![CDATA[{self.media_id}]]></MediaId>
            <Title><![CDATA[title]]></Title>
            <Description><![CDATA[description]]></Description>
        </Video>
        </xml>"""

