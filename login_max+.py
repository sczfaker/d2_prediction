#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import sys,io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

url = 'http://dotamax.com/accounts/login/'
headers = {'Host': 'dotamax.com', 'Connection': 'keep-alive', 'Content-Length': '1335', 'Cache-Control': 'max-age=0', 'Origin': 'http://dotamax.com', 'Upgrade-Insecure-Requests': '1', 'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.88 Safari/537.36 Vivaldi/2.4.1488.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'http://dotamax.com/accounts/logout/?src=bets', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9'}
cookies = {'_ga': 'GA1.2.917068991.1593764201', '_gid': 'GA1.2.981710910.1593764201', 'Hm_lvt_575895fe09d48554a608faa5ef059555': '1593764202', 'csrftoken': 'PP0Xh0PvPbiSWlk7tzkeVaJf7Cc9gUPe', '_gat': '1', 'Hm_lpvt_575895fe09d48554a608faa5ef059555': '1593768133'}
# data = {'csrfmiddlewaretoken': 'PP0Xh0PvPbiSWlk7tzkeVaJf7Cc9gUPe', 'phoneNumCipherb64': 'UI0XFR3urBNVZ2ZhsAP6fdKLZQqmCW13D4m3Ol0vAcpcSi4V8mU9k4T%2Bzw%2FLlDsE%0D%0A65LU0FXmRQFiSbgIwh%2FU%2F%2BNtI%2F2t0ULb8Pj29S%2BOwbCTzVdAu1kIEuNPOFIKllMy%0D%0ATvJ9MQLnw22CPRWWZIGY5QEPZPAgpwsk%2FftrmQ4QmL3X%2BU0PiJ1bBE0rXt8N%2BHXN%0D%0AEZaZ97w1En2umsVdwk4lSZrS%2Fg4iB%2Bgi82bwAx8oWIaL%2FHRBuFqxFYa1iCS4T6S9%0D%0AFf0bDFMMYdKvatLAvnnCP1HIwMOYPSddHgfOvVFLOdvm3Uo00vu%2Fh9ELNzHR%2Fz4g%0D%0AGKn5nlrcGyx3di1FR2sQMA%3D%3D', 'usernameCipherb64': 'Shga8IDmEK1HIIqZc3EGtVd4QpQtbC70aJOxA3La6SKzwqNsrx%2BblNY9LgOfreCr%0D%0AiGxBQdEgm0yKVja5RsIT4SMUSvIpf08xxGAwGK53KDwbRMuw3WMU4ZCJIAOaArMW%0D%0AiY8yb%2BsDFh%2BtKxOyW60MG3bYIVjDYWMwTeiGllqO%2FzsLMXJdlXhM2x%2BC5txlILjm%0D%0ALQAaBYMkW%2F%2BZt0YE9MwUyVIrBLcamhMaTM9jLzwV8DT289LAR7JCzDoWGP%2FHT%2FEz%0D%0AvNXm33KGhhhas3zYvvLrieUuA2nytbvtvJHZzmcn1aALuDzjWvDm%2FdCR1bnOQJj9%0D%0AnWZ1w3bVnI7imZFqd4%2B93Q%3D%3D', 'passwordCipherb64': 'YbFgL6BLlMLlX1s957%2FOBSbUiPIo3GUevWF%2BJAmPUrQDkHhicgZQKEnSkVQOnvSC%0D%0A8pmKhawfIjoRFP4hfWxhCSeDU6ZWlKyZc2zxQSkJE34FYKVgEjPdsq0lgB7mK%2BMS%0D%0ArL1c2l%2BZoHMWnz3sTf3EeIAljenoL4uKpc8l60uGkdYjdQZ%2Fg9hJB4KQp7BaSXYX%0D%0AbOSIaBppwHXPXdBoU%2BnIFUMff91QS8SO%2FklN5T5cswRKW60mxeMuiEhVQXQCTEDL%0D%0AtpsMAVWJgyH15292A2YuAahVT6u5BstvkXxUN5fQEQUGKYhHFKWBV2SmYDVWE0te%0D%0Ad04vmBSkUmoms%2BvD1cj4Lg%3D%3D', 'account-type': '2', 'src': 'bets'}
data={}

html = requests.post(url, headers=headers, verify=False, cookies=cookies, data={})
print(len(html.text))
print(html.text)
