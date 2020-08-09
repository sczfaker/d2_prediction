#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests

url = 'http://replay236.wmsj.cn/570/5536512014_842614051.dem.bz2'
headers = {'Host': 'replay236.wmsj.cn', 'Proxy-Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.88 Safari/537.36 Vivaldi/2.4.1488.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Range': 'bytes=32768-32768', 'If-Range': '"5f1d44c4-3981e6c"'}
cookies = {}
data = {}

html = requests.get(url,stream=True)
print (len(html.content))
with open ("x.dem.bz2","wb") as f:
	f.write(html.content)
	# for chunk in html.itere_content(chunk_size=1024):
	# 	if chunk:
	# 		f.write(chunk)


	# f.write(html.content)


# print(len(html.text))
# print(html.text)
