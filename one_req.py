from requests import get
from fake_useragent import UserAgent
ua = UserAgent()
headers={"User-Agent":ua.random,"Accept-Encoding":"gzip"}
x="https://liquipedia.net/dota2/Recast_Gaming"
t=get(x,headers=headers)
print (t.text)
