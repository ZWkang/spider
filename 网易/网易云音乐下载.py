# -*- coding:utf-8 -*-
#Author:周文康

import md5
import requests
import random
import json
from time import ctime,sleep
import multiprocessing
from bs4 import BeautifulSoup
import threading
import os

class Get_Mp3_Url(multiprocessing.Process):
	def __init__(self,queue,Lock,headers):
		multiprocessing.Process.__init__(self)
		self.queue = queue
		self.Lock = Lock
		self.headers = headers
	def run(self):
		while(self.queue.qsize()>0):
			groupids = self.queue.get()
			songslist  = self.Get_Message(self.Get_Url_Content("http://music.163.com/api/playlist/detail?"+str(groupids)),groupids)
			for i in xrange(len(songslist)):
				self.download(songslist[i][1],songslist[i][0],songslist[i][3],songslist[i][2])
		

	def Get_Url_Content(self,url):
		return requests.get(url,headers=random.choice(self.headers)).content

	def Get_Message(self,content,groupid):
		os.makedirs( "D:/wangyi/test/"+groupid)
		d = len(json.loads(content)['result']['tracks'])
		print d
		lists = [[] for i in xrange(d)]
		for i in xrange(d):
			try:
				lists[i].append(groupid)
				lists[i].append(str(json.loads(content)['result']['tracks'][i]['hMusic']['dfsId']))
				lists[i].append(json.loads(content)['result']['tracks'][i]['name'])
				lists[i].append(json.loads(content)['result']['tracks'][i]['id'])
			except Exception:
				lists[i].append(str(json.loads(content)['result']['tracks'][i]['bMusic']['dfsId']))
				lists[i].append(groupid)
				lists[i].append(json.loads(content)['result']['tracks'][i]['name'])
				lists[i].append(json.loads(content)['result']['tracks'][i]['id'])
		return lists
	def download(self,dfsid,group_id,song_id,name):
		url = 'http://m2.music.126.NET/%s/%s.mp3'%(self.encryptedid(dfsid),dfsid)
		r=requests.get(url,stream=True)

		with open("~/wangyi/test/%s/%s.mp3"%(group_id,name), 'wb') as f:  
		         for chunk in r.iter_content(chunk_size=1024):  
		            if chunk: # filter out keep-alive new chunks  
		                f.write(chunk)  
		                f.flush()  
		         f.close()
		return False

	def encryptedid(self,song_id):
		byte1 = bytearray('3go8&$8*3*3h0k(2)2')
		byte2 = bytearray(song_id)
		byte1_len = len(byte1)
		for i in xrange(len(byte2)):
		    byte2[i] = byte2[i]^byte1[i%byte1_len]
		m = md5.new()
		m.update(byte2)
		result = m.digest().encode('base64')[:-1]
		result = result.replace('/', '_')
		result = result.replace('+', '-')
		return result


if __name__ == '__main__':
	mul_queue = multiprocessing.Queue()
	mul_Lock = multiprocessing.Lock()
	headers = [
			{'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
			{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
			{'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
			{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
			{'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
			{'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}]



	for i in range(4):
		s = requests.Session()
		gedanurl = 'http://music.163.com/discover/playlist/?order=hot&cat=华语&limit=35&offset='+str(35*i)
		print gedanurl+' is ok'
		gedan_url = BeautifulSoup(s.get(gedanurl,headers=random.choice(headers)).content).select('.u-cover > a')
		for i in range(len(gedan_url)):
			mul_queue.put(str(gedan_url[i].attrs['href'].replace('/playlist?','')))
	print mul_queue.qsize()
	thread=[]


	for x in xrange(2):
		thread.append(Get_Mp3_Url(mul_queue,mul_Lock,headers))
	for y in thread:
		y.start()
	for i in thread:
		i.join()