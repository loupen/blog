# -*- coding: utf-8 -*-

import accessToken
import urllib.request


access_token = accessToken.GetAccessToken()
print(access_token)

postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % access_token

postMenu = """
{
	"button":
	[
		{
			"type": "click",
			"name": "开发指引",
			"key":  "mpGuide"
		},
	{
		"name": "公众平台",
		"sub_button":
		[
			{
				"type": "view",
				"name": "更新公告",
				"url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
			},
			{
				"type": "view",
				"name": "接口权限说明",
				"url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
			},
			{
				"type": "view",
				"name": "返回码说明",
				"url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433747234&token=&lang=zh_CN"
			}
		]
	},
	{
		"type": "media_id",
		"name": "旅行",
		"media_id": "z2zOokJvlzCXXNhSjF46gdx6rSghwX2xOD5GUV9nbX4"
	}
	]
}
"""

if isinstance(postMenu, str):
	postData = postMenu.encode('utf-8')
	urlResp = urllib.request.urlopen(url=postUrl, data=postData)
	print(urlResp.read())
