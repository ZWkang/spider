# -*- coding:utf-8 -*-
#Author:周文康
import requests
import sys
import random
import time
import threading
from bs4 import BeautifulSoup
import Queue
import sys
from time import ctime,sleep
reload(sys)
sys.setdefaultencoding('utf-8')


#快代理
def kuai():
	global lock
	print '快代理采集中'.decode('utf-8')
	kuaidaili = ['inha','intr','outha','outtr']
	#url的列表用于拼凑
	for x in range(len(kuaidaili)):
		for y in range(1,2):
		#range决定了要读取多少页   其实一般代理都是前面一些页面比较多可用的
			kuai_queue.put(y)
		if kuai_queue.qsize()==0:
			break
		while kuai_queue.qsize()>=1:
			url = 'http://www.kuaidaili.com/free/'+str(kuaidaili[x])+'/'+str(kuai_queue.get())
			# print url
			r = requests.get(url,headers=random.choice(headers))
			if r.status_code!=200:
				sleep(5)
				#设置一个定时休息因为错误有时候可能是过度频繁
			soup =  BeautifulSoup(r.content)
			# print r.content
			c = soup.find('table').find_all('td')
			for i in range(len(c)):
				if i%7==0:
					dailiurl=c[i+3].get_text().lower()+'://'+c[i].get_text()+':'+c[(i+1)].get_text()
					work_queue.put(dailiurl)
					#这个就没写。压入队列就可以了
					print dailiurl+' 采集成功'
				else:
					pass
	print '采集网页代理ip结束'.decode('utf-8')

#西刺
def xici():
	print '西刺采集进行中'.decode('utf-8')
	sleep(4)
	xici = ['nn','nt','wn','wt']
	global lock
	for x in range(len(xici)):
		for y in range(1,2):
			url = 'http://www.xicidaili.com/'+str(xici[x])+'/'+str(y)
			r = requests.get(url,headers=random.choice(headers))
			if r.status_code!=200:
				sleep(6)
				#设置一个定时休息因为错误有时候可能是过度频繁
			soup =  BeautifulSoup(r.content)
			c = soup.select('tr > td')
			for i in range(len(c)):
				if i%10==1:
					ipport=c[i+4].get_text().lower()+'://'+c[i].get_text()+':'+c[i+1].get_text()
					work_queue.put(ipport)
					lock.acquire()
					files = open('xiciIp.txt','a+')
					files.write(ipport+'\r\n')
					files.close()
					lock.release()
					#其实可以不写入文件的
					#可有可无吧
					print ipport+' 采集成功'
				else:
					pass
			# break
	
	print '采集xici网页代理ip结束'.decode('utf-8')
def isAlive(x):
	global lock
	threadname = str('线程-'+str(x+1))
	print 
	sleep(3)
	print (threadname+'-开启 测试开始').decode('utf-8').encode('gbk')
	# print work_queue.qsize()
	while work_queue.qsize()>0:
		url=work_queue.get()
		xxx = url.split(':')
		# url='http://123.124.168.149:80'
		proxies={xxx[0]:url}
		# print url
		try:
			r = requests.get('http://1212.ip138.com/ic.asp',proxies=proxies,timeout=15)
			if r.status_code==200:
				print threadname+'---'+url+(' 测试成功 写入文件 '.decode('utf-8'))
				lock.acquire()
				files = open('kuaiOK.txt','a+')
				files.write(url+'\r\n')
				files.close()
				lock.release()
			else:
				pass
		except Exception,e:
			# 
			# print Exception
			print threadname+'---'+url+' 测试失败 当前还有'+str(work_queue.qsize())+'待测试'.decode('utf-8')
			lock.acquire()
			files = open('httpbad.txt','a+')
			files.write(url+' unwork'+'\r\n')
			files.close()
			lock.release()
			# break
		# print '测试结束'
		# return False
	return False

if __name__ == '__main__':
	print 'start'
	headers = [
	    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
	    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
	    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
	    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
	    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
	    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
	]
	kuai_queue = Queue.Queue()
	#kuaiurl的地址池
	#其实可有可无的
	work_queue = Queue.Queue()
	#测试工作队列
	threads = []
	global lock
	#创建锁
	lock = threading.Lock()
	# 创建线程对象
	caijinumber = raw_input('选择开启采集进程个数'.decode('utf-8').encode('gbk'))
	testnumber = raw_input('选择开启测试进程个数'.decode('utf-8').encode('gbk'))

	num1=int(caijinumber)
	num2=int(testnumber)
	for x in xrange(0, num1):
		# t1 = 
		threads.append(threading.Thread(target=kuai))
		threads.append(threading.Thread(target=xici))
		#添加采集线程
		sleep(5)
	for x in xrange(0, num2):
		# t1 = 
		threads.append(threading.Thread(target=isAlive,args=(x,)))
		#添加测试线程
		# sleep(3)
	for t in threads:
		t.setDaemon(True)
		t.start()
	for t in threads:
		t.join() 