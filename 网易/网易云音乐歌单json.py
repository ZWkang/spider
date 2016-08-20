# -*- coding:utf-8 -*-
#Author:周文康
import requests
import sys
import random
from bs4 import BeautifulSoup
import Queue
from time import ctime,sleep
#爬取数据格式为json
#保存在本地文件名字为id=xxxxx.json


#
reload(sys)
sys.setdefaultencoding("utf-8")

#获得列表的歌单id
def getUrl(num):
	global urls
	for i in range(num):
		s = requests.Session()
		gedanurl = 'http://music.163.com/discover/playlist/?order=hot&cat=全部&limit=35&offset='+str(35*i)
		r = s.get(gedanurl,headers=random.choice(headers))
		print gedanurl+' is ok'
		soup =  BeautifulSoup(r.content)
		gedan_url = soup.select('.u-cover > a')
		for i in range(len(gedan_url)):
			urls.append(gedan_url[i].attrs['href'].replace('/playlist?',''))
def getJson(i_d):
	api_url='http://music.163.com/api/playlist/detail?'+str(i_d)
	sleep(2)
	ss = requests.get(api_url,headers=random.choice(headers))
	try:
		
		f = open(str(i_d)+'.json','a+')
		f.write(ss.content)
		f.close()
		print api_url+' is get'
	except Exception:
		print "写入文件失败"
if __name__ == '__main__':
	global headers,urls
	headers = [
			{'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
			{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
			{'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
			{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
			{'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
			{'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
	]
	urls = []
	numbers = raw_input('选择采集前几页的json,请不要大于总页数'.decode('utf-8').encode('gbk'))
	getUrl(int(numbers))
	for i in urls:
		getJson(i)
	