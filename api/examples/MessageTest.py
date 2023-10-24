# coding = utf-8

import random

from api.src.CorpApi import *
from configobj import ConfigObj

config = ConfigObj('../../config.ini', encoding='utf-8')

api = CorpApi(config['wechat']['CorpID'], config['wechat']['Secret'])

to_user = "momeak"
text = "这是一条测试消息"

try:
    response = api.httpCall(
        CORP_API_TYPE['MESSAGE_SEND'],
        {
            "touser": to_user,
            "agentid": config['wechat']['AgentId'],
            'msgtype': 'text',
            'climsgid': 'climsgidclimsgid_%f' % (random.random()),
            'text': {
                'content': text,
            },
            'safe': 0,
        })
    print(response)
except ApiException as e:
    print(e.errCode, e.errMsg)