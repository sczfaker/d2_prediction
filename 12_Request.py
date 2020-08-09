#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests

url = 'https://www.trackdota.com/matches/5557675466'
headers = {'Host': 'www.trackdota.com', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.88 Safari/537.36 Vivaldi/2.4.1488.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.dotabuff.com/esports', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9'}
cookies = {'_ga': 'GA1.2.54914190.1596865764', '_gid': 'GA1.2.497165365.1596865764', '_hjid': '455f154e-5b0c-47e9-a738-3b4e0287f99e', '_hjIncludedInCCSample': '1', '_hjIncludedInSample': '1'}
data = {}

html = requests.get(url, headers=headers, verify=False, cookies=cookies)
print(len(html.text))
print(html.text)
