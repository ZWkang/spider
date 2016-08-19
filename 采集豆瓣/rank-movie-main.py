# -*- coding:utf-8 -*-
#Author:周文康
#email:kang95630@gmail.com
#qq:907747874
import requests
import json
from time import sleep
import random
from bs4 import BeautifulSoup

#关键是这个是一个json的请求
#直接get得到json就ok了
#有32个分类
#评分有20种   其实重叠了一半   所以我取整数区间的评分的
#需要requests   beautifulsoup
#


headers = [
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
]

ranklist=['100%3A90','90%3A80','80%3A70','70%3A60','60%3A50','50%3A40','40%3A30','30%3A20','20%3A10','10%3A0']
types = range(1,33)
def openfile(values,msg):
	values = str(values)
	filename = 'type'+values+'.html'
	f = open(filename,'a+')
	f.write(msg.decode('utf-8').encode('utf-8'))
	f.close()
def getUrl(types,rank,start,limit):
	types = str(types)
	rank = str(rank)
	start=str(start)
	limit = str(limit)
	url = "https://movie.douban.com/j/chart/top_list?type="+types+"&interval_id="+rank+"&action=&start="+start+"&limit="+limit
	return url
def getPage(url,lists):
	# print type(list(lists))
	lists = list(lists)

	# print lists[1]
	r = requests.get(url, headers=random.choice(headers))
	if r.status_code != 200:
		sleep(400)
		getPage(url,lists)
	# s = json.loads(r.content)
	if r.content == '[]':
		print '**************************error     break   this rank************************'
		return False
	else:
		ss = str(lists[1])
		filenames = str(lists[0])+'-'+ss[-2:]
		openfile(filenames,r.content)
	print ""+url+"  is ok"
	return True
	# f.write(r.content.decode('utf-8').encode('utf-8'))

def startmain():
	for x in types:
		for i in ranklist:
			# print i
			for n in range(0,100):
				new_list=[x,i,n*200,200]
				# listss = ','.join(new_list)
				url = getUrl(x,i,n*200,200)
				print url
				if getPage(url,new_list):
					print '*****************************contiue  start**************************'
				else:
					print '******************************break   this   rank *************************'
					break

if __name__ == '__main__':
	startmain()