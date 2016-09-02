# -*- coding: utf-8 -*-
import requests
import random
from bs4 import BeautifulSoup
import time
from subprocess import Popen


headers={
    'Host': 'www.zhihu.com',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': '*/*',
    'Origin': 'https://www.zhihu.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
}
Zhihu_session = requests.Session()
rr = requests.get('http://www.zhihu.com/',headers=headers)

soup  =  BeautifulSoup(rr.content)
_xsrf = soup.find_all(attrs={'name':'_xsrf'})[0].attrs['value']
url_link = str(int(time.time()*1000))
captcha_url='http://www.zhihu.com/captcha.gif?r='+url_link+'&type=login'
#http://www.zhihu.com/captcha.gif?r='+url_link+'&type=login&lang=cn
r = Zhihu_session.get(captcha_url,headers =headers)


with open('code.gif','wb') as f:
	f.write(r.content)
Popen('code.gif',shell =True)
captcha =raw_input('captcha: ')
print captcha
data={"email":"xxx","password":"xxx","_xsrf":str(_xsrf),'remember_me':'true','captcha':captcha}
print Zhihu_session.post('https://www.zhihu.com/login/email',data=data,headers=headers).json()



