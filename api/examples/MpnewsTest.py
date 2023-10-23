# coding = utf-8

import random

from api.src.CorpApi import *
from configobj import ConfigObj

config = ConfigObj('../../config.ini', encoding='utf-8')

api = CorpApi(config['wechat']['CorpID'], config['wechat']['Secret'])

to_user = "WangZiCong|momeak"
text = "这是一条测试消息"

try:
    ##
    response = api.httpCall(
        CORP_API_TYPE['MESSAGE_SEND'],
        {
            "touser": to_user,
            "agentid": config['wechat']['AgentId'],
            'msgtype': 'news',
            'climsgid': 'climsgidclimsgid_%f' % (random.random()),
            'news': {
                'articles': [
                    {
                        "title": "中秋节礼品领取",
                        "description": "今年中秋节公司有豪礼相送",
                        "url": "URL",
                        "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png",
                        "btntxt": "更多"
                    },
                    {
                        "title": "中秋节礼品领取",
                        "description": "今年中秋节公司有豪礼相送",
                        "url": "URL",
                        "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png",
                        "btntxt": "更多"
                    }
                ]
            },
            'safe': 0,
        })
    print(response)
except ApiException as e:
    print(e.errCode, e.errMsg)
