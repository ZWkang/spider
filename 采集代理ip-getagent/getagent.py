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
def kuai(x):
	global lock
	print '快代理采集中     线程 ----'.decode('utf-8')+str(x)
	global kuaisss_queue
	
	#url的列表用于拼凑
	while kuaisss_url_queue.qsize()>0:
		url = kuaisss_url_queue.get()
		print kuaisss_url_queue.qsize()
		sleep(2)
		r = requests.get(url,headers=random.choice(headers))
		print r.status_code
		if r.status_code==503:
			print "状态码为503 ".decode('utf-8').encode('gbk')
			lock.acquire()
			f=open('kuaierror.txt','a+')
			f.write(time.strftime('%Y-%m-%d %H:%M:%S')+'    '+url+'   '+str(r.status_code)+'\n')
			f.close()
			lock.release()
			kuaisss_url_queue.put(url)
			#失败了再次压入kuai_url的队列里面等待运行
			# kuaisss_queue
			#设置一个定时休息因为错误有时候可能是过度频繁
		if r.status_code==200:
			soup =  BeautifulSoup(r.content)
			try:
				c = soup.select('#list > table')[0].find_all('td')
				lock.acquire()
				f=open('kuaisuccess.txt','a+')
				f.write(time.strftime('%Y-%m-%d %H:%M:%S')+'    '+url+'   '+str(r.status_code)+'\n')
				#写入正确日志
				f.close()
				lock.release()
			except:
				c=[]
				#这种时候一般是状态码不为200
			for i in range(len(c)):
				if i%7==0:
					dailiurl=c[i+3].get_text().lower()+'://'+c[i].get_text()+':'+c[(i+1)].get_text()
					work_queue.put(dailiurl)
					#这个就没写。压入队列就可以了
					print dailiurl+' 快采集成功'
				else:
					pass
	print '采集网页代理ip结束     线程 ---------'.decode('utf-8')+str(x)
	# sleep(2)

#西刺
def xici(x):
	print '西刺采集进行中      线程 ---------'.decode('utf-8')+str(x)
	global xici_url_queue
	global lock
	while xici_url_queue.qsize()>0:
		url=xici_url_queue.get()
		# print url
		sleep(2)
		r = requests.get(url,headers=random.choice(headers))
		# proxies = {""}
		if r.status_code!=200:
			print "状态码不为200 ".decode('utf-8').encode('gbk')
			lock.acquire()
			f=open('xicisuccess.txt','a+')
			f.write(time.strftime('%Y-%m-%d %H:%M:%S')+'    '+url+'   '+str(r.status_code)+'\n')
			f.close()
			xici_url_queue.put(url)
			lock.release()
			sleep(6)
			#设置一个定时休息因为错误有时候可能是过度频繁
		try:
			soup =  BeautifulSoup(r.content)
			c = soup.select('tr > td')
			lock.acquire()
			f=open('xicierror.txt','a+')
			f.write(time.strftime('%Y-%m-%d %H:%M:%S')+'    '+url+'   '+str(r.status_code)+'\n')
			f.close()
			lock.release()
		except Exception:
			c=[]
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
				print ipport+'西刺采集成功'
			else:
					pass
	print '采集xici网页代理ip结束'.decode('utf-8')
#http://www.cz88.net/
def getcz(x):
	global cz_queue
	print "采集 http://www.cz88.net/ 开始      线程 ---------".decode('utf-8')+str(x)
	url = ['index','http_']
	sleep(2)
	while cz_queue.qsize()>0:
		i=int(cz_queue.get())
		if i ==1:
			urls = 'http://www.cz88.net/proxy/'+str(url[0])+'.shtml'
		else:
			urls= 'http://www.cz88.net/proxy/'+url[1]+str(i)+'.shtml'
		# print urls
		print urls+'此页面采集开始'.decode('utf-8')
		# sleep(1)
		r = requests.get(urls,headers=random.choice(headers))
		if r.status_code!=200:
			print "状态码不为200 ".decode('utf-8').encode('gbk')
			sleep(6)
		soup = BeautifulSoup(r.content)
		iplen = soup.select('.ip')
		port = soup.select('.port')
		for i in range(1,len(iplen)):
			# print iplen[i].string
			ipports = 'http://'+iplen[i].string+':'+str(port[i].get_text())
			work_queue.put(ipports)
			print str(ipports)+' cz88采集成功'.decode('utf-8')
	print '采集cz99网页代理ip结束     线程 ---------'.decode('utf-8')+str(x)




def isAlive(x):
	global lock
	threadname = str('线程-'+str(x+1))
	sleep(90)
	print (threadname+'-开启 测试开始').decode('utf-8').encode('gbk')
	while work_queue.qsize()>0:
		url=work_queue.get()
		xxx = url.split(':')
		proxies={xxx[0]:url}
		# print url
		try:
			sleep(1)
			r = requests.get('http://1212.ip138.com/ic.asp',proxies=proxies,timeout=3)
			if r.status_code==200:
				print threadname+'---'+url+(' 测试成功 写入文件 '.decode('utf-8'))
				lock.acquire()
				files = open('TestOK.txt','a+')
				files.write(url+'\r\n')
				files.close()
				lock.release()
				#测试写入文件
			else:
				pass
		except Exception,e:
			# 
			print threadname+'---'+url+' 测试失败 当前还有'+str(work_queue.qsize())+'待测试'.decode('utf-8')
			lock.acquire()
			files = open('Testbad.txt','a+')
			files.write(url+' unwork'+'\r\n')
			files.close()
			lock.release()
			# break

	return False
lock = threading.Lock()
if __name__ == '__main__':
	start = time.clock()
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

	#锁是全局共享 线程也共享栈	
	# 创建线程对象
	caijinumber = raw_input('选择开启采集进程个数'.decode('utf-8').encode('gbk'))
	testnumber = raw_input('选择开启测试进程个数'.decode('utf-8').encode('gbk'))

	num1=int(caijinumber)
	num2=int(testnumber)
	
	

	#cz页面url队列生产
	cz_queue = Queue.Queue()
	for i in xrange(1,10):
		cz_queue.put(i)
	#kuai代理页面队列生产
	kuaisss_url_queue=Queue.Queue()
	kuaidaili = ['inha','intr','outha','outtr']
	for i in xrange(1,180):
		for x in xrange(len(kuaidaili)):
			kuaisss_url_queue.put('http://www.kuaidaili.com/free/'+str(kuaidaili[x])+'/'+str(i))
	
	# print kuaisss_url_queue.qsize()
	#西刺网站生产URL页面队列
	xici_url_queue=Queue.Queue()
	xici_types = ['nn','nt','wn','wt']
	for i in xrange(1,100):
		for page_type in xici_types:
			xici_url_queue.put('http://www.xicidaili.com/'+str(page_type)+'/'+str(i))


	# print xici_url_queue.qsize()

	for x in xrange(num1):
		threads.append(threading.Thread(target=kuai,args=(x,)))
		# 快代理
		threads.append(threading.Thread(target=xici,args=(x,)))
		#西刺
		threads.append(threading.Thread(target=getcz,args=(x,)))
		#添加采集线程

	for x in xrange(0, num2):

		threads.append(threading.Thread(target=isAlive,args=(x,)))
		# 添加测试线程
		# sleep(3)
	for t in threads:

		t.setDaemon(True)
		sleep(2)
		t.start()
	for t in threads:
		t.join() 
	for z in threads:
		print z.getName()
		print z.isAlive()
	end = time.clock()
	print 'Running time: %s Seconds'%(end-start)