# -*- coding: utf-8 -*-：
#好像很多bug可是不想改了
#结合前面的得到代理使用 
import requests
import json
import Queue
import threading
import random
from time import sleep
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
g_mutex=threading.Condition()
GangWeiLists = ["后端开发","移动开发","前端开发","测试","运维","DBA","高端职位","项目管理","硬件开发","企业软件","产品经理","产品设计师","高端职位","视觉设计","用户研究","高端职位","交互设计","运营","编辑","客服","高端职位","市场/营销","公关","销售","高端职位","供应链","采购","投资","人力资源","行政","财务","高端职位","法务","投融资","风控","审计税务","高端职位","Java","Python","PHP",".NET","C#","C++","C","VB","Delphi","Perl","Ruby","Hadoop","Node.js","数据挖掘","自然语言处理","搜索算法","精准推荐","全栈工程师","Go","ASP","Shell","后端开发其它","HTML5","Android","iOS","WP","移动开发其它","web前端","Flash","html5","JavaScript","U3D","COCOS2D-X","前端开发其它","测试工程师","自动化测试","功能测试","性能测试","测试开发","游戏测试","白盒测试","灰盒测试","黑盒测试","手机测试","硬件测试","测试经理","测试其它","运维工程师","运维开发工程师","网络工程师","系统工程师","IT支持","IDC","CDN","F5","系统管理员","病毒分析","WEB安全","网络安全","系统安全","运维经理","运维其它","MySQL","SQLServer","Oracle","DB2","MongoDB","ETL","Hive","数据仓库","DBA其它","技术经理","技术总监","架构师","CTO","运维总监","技术合伙人","项目总监","测试总监","安全专家","高端技术职位其它","项目经理","项目助理","硬件","嵌入式","自动化","单片机","电路设计","驱动开发","系统集成","FPGA开发","DSP开发","ARM开发","PCB工艺","模具设计","热传导","材料工程师","精益工程师","射频工程师","硬件开发其它","实施工程师","售前工程师","售后工程师","BI工程师","企业软件其它","产品经理","网页产品经理","移动产品经理","产品助理","数据产品经理","电商产品经理","游戏策划","产品实习生","网页产品设计师","无线产品设计师","产品部经理","产品总监","游戏制作人","网页设计师","Flash设计师","APP设计师","UI设计师","平面设计师","美术设计师（2D/3D）","广告设计师","多媒体设计师","原画师","游戏特效","游戏界面设计师","视觉设计师","游戏场景","游戏角色","游戏动作","数据分析师","用户研究员","游戏数值策划","设计经理/主管","设计总监","视觉设计经理/主管","视觉设计总监","交互设计经理/主管","交互设计总监","用户研究经理/主管","用户研究总监","网页交互设计师","交互设计师","无线交互设计师","硬件交互设计师","内容运营","产品运营","数据运营","用户运营","活动运营","商家运营","品类运营","游戏运营","网络推广","运营专员","网店运营","新媒体运营","海外运营","运营经理","副主编","内容编辑","文案策划","记者","售前咨询","售后客服","淘宝客服","客服经理","主编","运营总监","COO","客服总监","市场策划","市场顾问","市场营销","市场推广","SEO","SEM","商务渠道","商业数据分析","活动策划","网络营销","海外市场","政府关系","媒介经理","广告协调","品牌公关","销售专员","销售经理","客户代表","大客户代表","BD经理","商务渠道","渠道销售","代理商销售","销售助理","电话销售","销售顾问","商品经理","市场总监","销售总监","商务总监","CMO","公关总监","采购总监","投资总监","物流","仓储","采购专员","采购经理","商品经理","分析师","投资顾问","投资经理","人事/HR","培训经理","薪资福利经理","绩效考核经理","人力资源","招聘","HRBP","员工关系","助理","前台","行政","总助","文秘","会计","出纳","财务","结算","税务","审计","风控","行政总监/经理","财务总监/经理","HRD/HRM","CFO","CEO","法务","律师","专利","投资经理","分析师","投资助理","融资","并购","行业研究","投资者关系","资产管理","理财顾问","交易员","风控","资信评估","合规稽查","律师","审计","法务","会计","清算","投资总监","融资总监","并购总监","风控总监","副总裁"]
cate_queue = Queue.Queue()
exist_queue = []
proxies_pool = Queue.Queue()

class Crawer(threading.Thread):
	def __init__(self,filename,tid,proxies_s):
		threading.Thread.__init__(self)
		# self.url = url
		self.filename=filename
		self.tid=tid
		self.proxies={"http":proxies_s}
		print str(self.tid)+' is start  当前使用代理ip'.decode('utf-8').encode('gbk')+str(self.proxies)
	def run(self):
		global cate_queue
		global exist_queue
		_cookies = self.getCookie()
		_headers = self.GetHea()
		while(cate_queue.qsize()>0):
			sleep(2)
			url = cate_queue.get()
			Html_Info = self.GetUrlInfo(url,_headers,_cookies)
			if Html_Info:
				if self.write(self.filename,Html_Info):
					g_mutex.acquire()
					f=open('exists_url.txt',"a+")
					f.write(url)
					f.close()
					g_mutex.release()
			else:
				return False
		return False

	def GetUrlInfo(self,url,h,c):
		try:
			_Info = requests.get(url,headers=h,cookies=c,proxies=self.proxies,timeout=10).content
			if len(json.loads(_Info)["content"]["positionResult"]["result"]):
				print len(json.loads(_Info)["content"]["positionResult"]["result"])
				return _Info
			else:
				print len(json.loads(_Info)["content"]["positionResult"]["result"])
				return False
		except Exception:
			print self.proxies
			self.change_proxies()
			self.GetUrlInfo(url,h,c)
			print '123123123'
		# return _Info


	def change_proxies(self):
		global proxies_pool
		if proxies_pool.qsize()>0:
			self.proxies={"http":proxies_pool.get().replace('\r\n','')}
			print str(self.tid)+str(self.proxies)+' 改变当前使用代理ip'.decode('utf-8').encode('gbk')
	def GetHea(self):
		header_s = [
		           {'User-Agent': 'Mozilla/6.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
		           {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
		           {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},
		           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
		           {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
		           {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
		           {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
		]
		return random.choice(header_s)
	def getCookie(self):
		return requests.get('http://www.lagou.com').cookies
	def write(self,filename,message):
		global g_mutex
		g_mutex.acquire()
		f = open(filename+'.txt',"a+")
		f.write(message+'\n')
		f.close()
		g_mutex.release()
		return True

# def getURL
def GetUrls(category_name,h={'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}):
	global size_s
	print category_name.decode('utf-8').encode('gbk')
	# proxies = {'http':'http://122.96.59.104:80'}
	global proxies_pool
	# replace
	url = 'http://www.lagou.com/jobs/positionAjax.json?city=全国&first=false&kd=%s&pn=1'%GangWeiLists[0]
	_proxies = {'http':proxies_pool.get().replace('\r\n','')}
	print _proxies
	try:
		counts = json.loads(requests.get(url,headers=h,cookies=getCookie(),proxies=_proxies,timeout=10).content)
		print counts
		print 'lalal'
		size_s = counts['content']['positionResult']['totalCount']
		print size_s

	except Exception:
		GetUrls(category_name,h)	
	return size_s
	
	

def getCookie():
	return requests.get('http://www.lagou.com').cookies


class csss:
	def __init__(self,name):
		self.name=name
	def setName(self,value):
		self.name=value
	def getName(self):
		print self.name


def queue_ss():
	return False

if __name__ == '__main__':
	


	for d in xrange(4,len(GangWeiLists)):
		f = open("kuaiOK.txt",'r')
		for line in f:
			if line !='':
				proxies_pool.put(line)
		print proxies_pool.qsize()
		sizess = GetUrls(GangWeiLists[d])

		a  = int(sizess)/15
		threads=[]
		for i in xrange(1,a+1):
			cate_queue.put('http://www.lagou.com/jobs/positionAjax.json?city=全国&first=false&kd=%s&pn=%d'%(GangWeiLists[d],i))
		# sleep(10)
		# print d
		# print GangWeiLists[i]
		for c in xrange(10):
			threads.append(Crawer(GangWeiLists[d].decode('utf-8').encode('gbk'),c,proxies_pool.get().replace('\r\n','')))
		for x in threads:
			x.start()
		for x in threads:
			x.join()
	# print proxies_pool.get()






