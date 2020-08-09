#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests

url = 'http://kuaikegame.com/api/steam/dota/series/getDota2SeriesDtlPageInfo.do?seriesPkId=db84604b-3b5a-4439-b296-331f0f6cb2ab'
headers = {'Host': 'kuaikegame.com', 'Connection': 'keep-alive', 'Accept': 'application/json, text/plain, */*', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.88 Safari/537.36 Vivaldi/2.4.1488.36', 'Referer': 'http://kuaikegame.com/', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9'}
cookies = {}
data = {}

html = requests.get(url, headers=headers, verify=False, cookies=cookies)
print(len(html.text))
print(html.text)
