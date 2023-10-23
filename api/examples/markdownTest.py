# coding = utf-8

import random

from api.src.CorpApi import *
from configobj import ConfigObj

config = ConfigObj('../../config.ini', encoding='utf-8')

api = CorpApi(config['wechat']['CorpID'], config['wechat']['Secret'])

to_user = "WangZiCong|momeak"

markdownContent = """
您的会议室已经预定，稍后会同步到`邮箱`
>**事项详情**
>事　项：<font color=\"info\">开会</font>
>组织者：@miglioguan
>参与者：@miglioguan、@kunliu、@jamdeezhou、@kanexiong、@kisonwang
>
>会议室：<font color=\"info\">广州TIT 1楼 301</font>
>日　期：<font color=\"warning\">2018年5月18日</font>
>时　间：<font color=\"comment\">上午9:00-11:00</font>
>
>请准时参加会议。
>
>如需修改会议信息，请点击：[修改会议信息](https://work.weixin.qq.com)
"""

try:
    ##
    response = api.httpCall(
        CORP_API_TYPE['MESSAGE_SEND'],
        {
            "touser": to_user,
            "agentid": config['wechat']['AgentId'],
            'msgtype': 'markdown',
            'climsgid': 'climsgidclimsgid_%f' % (random.random()),
            'markdown': {
                'content': markdownContent,
            },
            'safe': 0,
        })
    print(response)
except ApiException as e:
    print(e.errCode, e.errMsg)

