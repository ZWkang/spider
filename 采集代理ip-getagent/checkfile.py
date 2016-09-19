# -*- coding:utf-8 -*-
#Author:周文康
import requests
import sys
import random
import time
import threading
import Queue
import sys
from time import ctime,sleep



work_queue=Queue.Queue()
lock = threading.Lock()
def isAlive(x):
	global lock
	threadname = str('线程-'+str(x+1))
	# sleep(10)
	print (threadname+'-开启 测试开始').decode('utf-8').encode('gbk')
	# print work_queue.qsize()
	while work_queue.qsize()>0:
		url=work_queue.get().replace('\r\n','').replace('\n','')
		# print url
		# xxx = url.split(':')
		# print url
		proxies={'http':str(url)}
		# print url
		# break
		# print url
		try:
			r = requests.get('http://1212.ip138.com/ic.asp',proxies=proxies,timeout=5)
			if r.status_code==200:
				print url+' is ok'
				lock.acquire()
				files = open('testokss.txt','a+')
				files.write(url+'\r\n')
				files.close()
				lock.release()
			else:
				pass
		except Exception,e:
			# 
			# print Exception
			# print e
			# print url
			lock.acquire()
			files = open('httpbads.txt','a+')
			files.write(url+' unwork'+'\r\n')
			files.close()
			lock.release()
			# break
		# print '测试结束'
		# return False
	return False


if __name__ == '__main__':
	threads=[]
	filename = str(raw_input('请输入你想要测试的文件'.decode('utf-8').encode('gbk')))
	f = open("TestOK.txt",'r') 
	line = f.readline()
	while line!='':
		# print line.split(':')[0]
		work_queue.put(line)
		line = f.readline()

	f.close()

	# sleep(5)
	for x in xrange(20):
		threads.append(threading.Thread(target=isAlive,args=(x,)))
	for i in threads:
		i.start()
	for s in threads:
		s.join()