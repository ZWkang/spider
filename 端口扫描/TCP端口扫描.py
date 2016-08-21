# -*- coding:utf-8 -*-
#Author:周文康
import socket
import os
import sys
from time import ctime,sleep
import multiprocessing
import threading
import Queue
import time

#目前只能扫描TCP端口
reload(sys)
sys.setdefaultencoding('utf-8')


class ClockProcess(multiprocessing.Process):
	def __init__(self, name,ip_des,work_qq,lock):
		multiprocessing.Process.__init__(self)
		self.name = name
		self.ip_des = ip_des
		self.work_qq = work_qq
		self.lock=lock
	def run(self):
		goodport=[]
		print("thread  "+self.name+str(self.pid)+'----'+' is start')
		sleep(1)
		timeout=10
		goodport.append(self.ip_des)
		while self.work_qq.qsize()>0:
			socket.setdefaulttimeout(timeout)
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:	
				p_ort = self.work_qq.get()
				s.connect((str(self.ip_des),int(p_ort)))
				goodport.append(str(self.ip_des)+':'+str(p_ort))
				print str(self.ip_des)+':'+str(p_ort)+' is ok'
			except Exception:
				pass
			s.close()
		self.lock.acquire()
		try:
			if len(goodport)>1:
				f= open(self.ip_des+'.txt','a+')
				f.write(str(goodport))
				f.close()	
		
		finally:
			self.lock.release()
			print 'done'
		self.close()
			

def testIpPort(ip_des,work):
	global locks
	# print 'start'
	timeout=10
	while work.qsize()>0:
		socket.setdefaulttimeout(timeout)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:	
			port = work.get()
			s.connect((ip_des,int(port)))
			locks.acquire()
			f = open(str(ip_des)+'.txt','a+')
			f.write(str(port)+':')
			f.close()
			locks.release()
			print str(port)+'ok'
		except Exception:
			pass
		s.close()
	print 'stopping'
	return False

if __name__ == '__main__':
	global locks
	ip_s = raw_input('选择扫描的ip:         '.decode('utf-8').encode('gbk'))
	number = raw_input('请选择多进程还是多线程,多进程选1,多线程选2:         '.decode('utf-8').encode('gbk'))
	try:
		if int(number)==1:
			mul_thread_number= raw_input('请填写创建进程数(填写数字):         '.decode('utf-8').encode('gbk'))
		elif int(number)==2:
			mul_thread_number= raw_input('请填写创建线程数(填写数字):         '.decode('utf-8').encode('gbk'))
		else:
			print "填写格式有误".decode('utf-8').encode('gbk')
			sys.exit()
	except Exception:
		print('填写格式有误'.decode('utf-8').encode('gbk'))
		sys.exit()
	numbers = raw_input('请输入扫描端口范围,格式1-88:            '.decode('utf-8').encode('gbk'))
	try:
		int(mul_thread_number)

		int(number)
	except Exception:
		print "填写格式有误".decode('utf-8').encode('gbk')
		sys.exit()


	if int(number) ==1:
		thread=[]
		ports = numbers.split("-")
		work_q = multiprocessing.Queue()
		lock = multiprocessing.Lock()
		for i in range(int(ports[0]),int(ports[1])):
			work_q.put(i)
			# print i
		sleep(1)

		for i in xrange(int(mul_thread_number)):
			thread.append(ClockProcess('kang',ip_s,work_q,lock))
		for i in thread:
			i.start()
			print str(i.pid)+' is start'
		for i in thread:
			i.join()	
	elif int(number)==2:
		thread=[]
		locks = threading.Lock()
		work_queue = Queue.Queue()
		ports = numbers.split("-")
		for i in xrange(int(ports[0]),int(ports[1])):
			work_queue.put(i)
		for x in xrange(int(mul_thread_number)):
			thread.append(threading.Thread(target=testIpPort,args=(ip_s,work_queue,)))
		for i in thread:
			print i.getName()
			# i.setDaemon(True)
			i.start()
			# sleep(2)
		for i in thread:
			i.join
		
		
	else:
		print 'error enter'
