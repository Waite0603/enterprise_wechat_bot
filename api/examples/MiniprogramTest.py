# coding = utf-8
import random

from api.src.CorpApi import *
from configobj import ConfigObj

config = ConfigObj('../../config.ini', encoding='utf-8')

api = CorpApi(config['wechat']['CorpID'], config['wechat']['Secret'])

to_user = "momeak"

try:
    response = api.httpCall(
        CORP_API_TYPE['MESSAGE_SEND'],
        {
            'touser': to_user,
            'agentid': config['wechat']['AgentId'],
            'msgtype': 'miniprogram_notice',
            'climsgid': 'climsgidclimsgid_%f' % (random.random()),
            'miniprogram_notice': {
                'appid': 'wx123123123123123',
                'page': 'pages/index?userid=zhangsan&orderid=123123123',
                'title': '会议室预订成功通知',
                'description': '4月27日 16:16',
                'emphasis_first_item': True,
                'content_item': [
                    {
                        'key': '会议室',
                        'value': '402'
                    },
                    {
                        'key': '会议地点',
                        'value': '广州TIT-402会议室'
                    },
                    {
                        'key': '会议时间',
                        'value': '2018年8月1日 09:00-09:30'
                    },
                    {
                        'key': '参与人员',
                        'value': '周剑轩'
                    }
                ]
            },
            'safe': 0,
        })
    print(response)
except ApiException as e:
    print(e.errCode, e.errMsg)