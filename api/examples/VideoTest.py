# coding = utf-8

import random

from api.src.CorpApi import *
from configobj import ConfigObj

config = ConfigObj('../../config.ini', encoding='utf-8')

api = CorpApi(config['wechat']['CorpID'], config['wechat']['Secret'])

# 以下为调用临时素材上传接口, 如需使用建议封装, 文档: https://developer.work.weixin.qq.com/document/path/90253
path = "exam.mp4"
title = "example_title"
description = "example_description"
img_url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={}&type=video".format(api.getAccessToken())
files = {'video': open(path, 'rb')}
r = requests.post(img_url, files=files)
re = json.loads(r.text)
print(re)
media_id = re['media_id']

to_user = "momeak"

try:
    ##
    response = api.httpCall(
        CORP_API_TYPE['MESSAGE_SEND'],
        {
            "touser": to_user,
            "agentid": config['wechat']['AgentId'],
            'msgtype': 'video',
            'climsgid': 'climsgidclimsgid_%f' % (random.random()),
            'video': {
                "title": title,
                "description": description,
                "media_id": media_id
            },
            'safe': 0,
        })
    print(response)
except ApiException as e:
    print(e.errCode, e.errMsg)
