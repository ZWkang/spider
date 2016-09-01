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
import urllib


reload(sys)
sys.setdefaultencoding('utf-8')


# g_mutex=threading.Condition()
g_mutex=threading.Lock()


proxies_pool = Queue.Queue() 
proxies_pool = Queue.Queue() 
GangWeiLists = ["Android","iOS","WP","移动开发其它","web前端","Flash","html5","JavaScript","U3D","COCOS2D-X","前端开发其它","测试工程师","自动化测试","功能测试","性能测试","测试开发","游戏测试","白盒测试","灰盒测试","黑盒测试","手机测试","硬件测试","测试经理","测试其它","运维工程师","运维开发工程师","网络工程师","系统工程师","IT支持","IDC","CDN","F5","系统管理员","病毒分析","WEB安全","网络安全","系统安全","运维经理","运维其它","MySQL","SQLServer","Oracle","DB2","MongoDB","ETL","Hive","数据仓库","DBA其它","技术经理","技术总监","架构师","CTO","运维总监","技术合伙人","项目总监","测试总监","安全专家","高端技术职位其它","项目经理","项目助理","硬件","嵌入式","自动化","单片机","电路设计","驱动开发","系统集成","FPGA开发","DSP开发","ARM开发","PCB工艺","模具设计","热传导","材料工程师","精益工程师","射频工程师","硬件开发其它","实施工程师","售前工程师","售后工程师","BI工程师","企业软件其它","产品经理","网页产品经理","移动产品经理","产品助理","数据产品经理","电商产品经理","游戏策划","产品实习生","网页产品设计师","无线产品设计师","产品部经理","产品总监","游戏制作人","网页设计师","Flash设计师","APP设计师","UI设计师","平面设计师","美术设计师（2D/3D）","广告设计师","多媒体设计师","原画师","游戏特效","游戏界面设计师","视觉设计师","游戏场景","游戏角色","游戏动作","数据分析师","用户研究员","游戏数值策划","设计经理/主管","设计总监","视觉设计经理/主管","视觉设计总监","交互设计经理/主管","交互设计总监","用户研究经理/主管","用户研究总监","网页交互设计师","交互设计师","无线交互设计师","硬件交互设计师","内容运营","产品运营","数据运营","用户运营","活动运营","商家运营","品类运营","游戏运营","网络推广","运营专员","网店运营","新媒体运营","海外运营","运营经理","副主编","内容编辑","文案策划","记者","售前咨询","售后客服","淘宝客服","客服经理","主编","运营总监","COO","客服总监","市场策划","市场顾问","市场营销","市场推广","SEO","SEM","商务渠道","商业数据分析","活动策划","网络营销","海外市场","政府关系","媒介经理","广告协调","品牌公关","销售专员","销售经理","客户代表","大客户代表","BD经理","商务渠道","渠道销售","代理商销售","销售助理","电话销售","销售顾问","商品经理","市场总监","销售总监","商务总监","CMO","公关总监","采购总监","投资总监","物流","仓储","采购专员","采购经理","商品经理","分析师","投资顾问","投资经理","人事/HR","培训经理","薪资福利经理","绩效考核经理","人力资源","招聘","HRBP","员工关系","助理","前台","行政","总助","文秘","会计","出纳","财务","结算","税务","审计","风控","行政总监/经理","财务总监/经理","HRD/HRM","CFO","CEO","法务","律师","专利","投资经理","分析师","投资助理","融资","并购","行业研究","投资者关系","资产管理","理财顾问","交易员","风控","资信评估","合规稽查","律师","审计","法务","会计","清算","投资总监","融资总监","并购总监","风控总监","副总裁"]
# GangWeiLists=["Java","Python","PHP",".NET","C%23","C%2B%2B","C","VB","Delphi","Perl","Ruby","Hadoop","Node.js","%CA%FD%BE%DD%CD%DA%BE%F2","%D7%D4%C8%BB%D3%EF%D1%D4%B4%A6%C0%ED","%CB%D1%CB%F7%CB%E3%B7%A8","%BE%AB%D7%BC%CD%C6%BC%F6","%C8%AB%D5%BB%B9%A4%B3%CC%CA%A6","Go","ASP","Shell","%BA%F3%B6%CB%BF%AA%B7%A2%C6%E4%CB%FC","HTML5","Android","iOS","WP","%D2%C6%B6%AF%BF%AA%B7%A2%C6%E4%CB%FC","web%C7%B0%B6%CB","Flash","html5","JavaScript","U3D","COCOS2D-X","%C7%B0%B6%CB%BF%AA%B7%A2%C6%E4%CB%FC","%B2%E2%CA%D4%B9%A4%B3%CC%CA%A6","%D7%D4%B6%AF%BB%AF%B2%E2%CA%D4","%B9%A6%C4%DC%B2%E2%CA%D4","%D0%D4%C4%DC%B2%E2%CA%D4","%B2%E2%CA%D4%BF%AA%B7%A2","%D3%CE%CF%B7%B2%E2%CA%D4","%B0%D7%BA%D0%B2%E2%CA%D4","%BB%D2%BA%D0%B2%E2%CA%D4","%BA%DA%BA%D0%B2%E2%CA%D4","%CA%D6%BB%FA%B2%E2%CA%D4","%D3%B2%BC%FE%B2%E2%CA%D4","%B2%E2%CA%D4%BE%AD%C0%ED","%B2%E2%CA%D4%C6%E4%CB%FC","%D4%CB%CE%AC%B9%A4%B3%CC%CA%A6","%D4%CB%CE%AC%BF%AA%B7%A2%B9%A4%B3%CC%CA%A6","%CD%F8%C2%E7%B9%A4%B3%CC%CA%A6","%CF%B5%CD%B3%B9%A4%B3%CC%CA%A6","IT%D6%A7%B3%D6","IDC","CDN","F5","%CF%B5%CD%B3%B9%DC%C0%ED%D4%B1","%B2%A1%B6%BE%B7%D6%CE%F6","WEB%B0%B2%C8%AB","%CD%F8%C2%E7%B0%B2%C8%AB","%CF%B5%CD%B3%B0%B2%C8%AB","%D4%CB%CE%AC%BE%AD%C0%ED","%D4%CB%CE%AC%C6%E4%CB%FC","MySQL","SQLServer","Oracle","DB2","MongoDB","ETL","Hive","%CA%FD%BE%DD%B2%D6%BF%E2","DBA%C6%E4%CB%FC","%BC%BC%CA%F5%BE%AD%C0%ED","%BC%BC%CA%F5%D7%DC%BC%E0","%BC%DC%B9%B9%CA%A6","CTO","%D4%CB%CE%AC%D7%DC%BC%E0","%BC%BC%CA%F5%BA%CF%BB%EF%C8%CB","%CF%EE%C4%BF%D7%DC%BC%E0","%B2%E2%CA%D4%D7%DC%BC%E0","%B0%B2%C8%AB%D7%A8%BC%D2","%B8%DF%B6%CB%BC%BC%CA%F5%D6%B0%CE%BB%C6%E4%CB%FC","%CF%EE%C4%BF%BE%AD%C0%ED","%CF%EE%C4%BF%D6%FA%C0%ED","%D3%B2%BC%FE","%C7%B6%C8%EB%CA%BD","%D7%D4%B6%AF%BB%AF","%B5%A5%C6%AC%BB%FA","%B5%E7%C2%B7%C9%E8%BC%C6","%C7%FD%B6%AF%BF%AA%B7%A2","%CF%B5%CD%B3%BC%AF%B3%C9","FPGA%BF%AA%B7%A2","DSP%BF%AA%B7%A2","ARM%BF%AA%B7%A2","PCB%B9%A4%D2%D5","%C4%A3%BE%DF%C9%E8%BC%C6","%C8%C8%B4%AB%B5%BC","%B2%C4%C1%CF%B9%A4%B3%CC%CA%A6","%BE%AB%D2%E6%B9%A4%B3%CC%CA%A6","%C9%E4%C6%B5%B9%A4%B3%CC%CA%A6","%D3%B2%BC%FE%BF%AA%B7%A2%C6%E4%CB%FC","%CA%B5%CA%A9%B9%A4%B3%CC%CA%A6","%CA%DB%C7%B0%B9%A4%B3%CC%CA%A6","%CA%DB%BA%F3%B9%A4%B3%CC%CA%A6","BI%B9%A4%B3%CC%CA%A6","%C6%F3%D2%B5%C8%ED%BC%FE%C6%E4%CB%FC","%B2%FA%C6%B7%BE%AD%C0%ED","%CD%F8%D2%B3%B2%FA%C6%B7%BE%AD%C0%ED","%D2%C6%B6%AF%B2%FA%C6%B7%BE%AD%C0%ED","%B2%FA%C6%B7%D6%FA%C0%ED","%CA%FD%BE%DD%B2%FA%C6%B7%BE%AD%C0%ED","%B5%E7%C9%CC%B2%FA%C6%B7%BE%AD%C0%ED","%D3%CE%CF%B7%B2%DF%BB%AE","%B2%FA%C6%B7%CA%B5%CF%B0%C9%FA","%CD%F8%D2%B3%B2%FA%C6%B7%C9%E8%BC%C6%CA%A6","%CE%DE%CF%DF%B2%FA%C6%B7%C9%E8%BC%C6%CA%A6","%B2%FA%C6%B7%B2%BF%BE%AD%C0%ED","%B2%FA%C6%B7%D7%DC%BC%E0","%D3%CE%CF%B7%D6%C6%D7%F7%C8%CB","%CD%F8%D2%B3%C9%E8%BC%C6%CA%A6","Flash%C9%E8%BC%C6%CA%A6","APP%C9%E8%BC%C6%CA%A6","UI%C9%E8%BC%C6%CA%A6","%C6%BD%C3%E6%C9%E8%BC%C6%CA%A6","%C3%C0%CA%F5%C9%E8%BC%C6%CA%A6%A3%A82D/3D%A3%A9","%B9%E3%B8%E6%C9%E8%BC%C6%CA%A6","%B6%E0%C3%BD%CC%E5%C9%E8%BC%C6%CA%A6","%D4%AD%BB%AD%CA%A6","%D3%CE%CF%B7%CC%D8%D0%A7","%D3%CE%CF%B7%BD%E7%C3%E6%C9%E8%BC%C6%CA%A6","%CA%D3%BE%F5%C9%E8%BC%C6%CA%A6","%D3%CE%CF%B7%B3%A1%BE%B0","%D3%CE%CF%B7%BD%C7%C9%AB","%D3%CE%CF%B7%B6%AF%D7%F7","%CA%FD%BE%DD%B7%D6%CE%F6%CA%A6","%D3%C3%BB%A7%D1%D0%BE%BF%D4%B1","%D3%CE%CF%B7%CA%FD%D6%B5%B2%DF%BB%AE","%C9%E8%BC%C6%BE%AD%C0%ED/%D6%F7%B9%DC","%C9%E8%BC%C6%D7%DC%BC%E0","%CA%D3%BE%F5%C9%E8%BC%C6%BE%AD%C0%ED/%D6%F7%B9%DC","%CA%D3%BE%F5%C9%E8%BC%C6%D7%DC%BC%E0","%BD%BB%BB%A5%C9%E8%BC%C6%BE%AD%C0%ED/%D6%F7%B9%DC","%BD%BB%BB%A5%C9%E8%BC%C6%D7%DC%BC%E0","%D3%C3%BB%A7%D1%D0%BE%BF%BE%AD%C0%ED/%D6%F7%B9%DC","%D3%C3%BB%A7%D1%D0%BE%BF%D7%DC%BC%E0","%CD%F8%D2%B3%BD%BB%BB%A5%C9%E8%BC%C6%CA%A6","%BD%BB%BB%A5%C9%E8%BC%C6%CA%A6","%CE%DE%CF%DF%BD%BB%BB%A5%C9%E8%BC%C6%CA%A6","%D3%B2%BC%FE%BD%BB%BB%A5%C9%E8%BC%C6%CA%A6","%C4%DA%C8%DD%D4%CB%D3%AA","%B2%FA%C6%B7%D4%CB%D3%AA","%CA%FD%BE%DD%D4%CB%D3%AA","%D3%C3%BB%A7%D4%CB%D3%AA","%BB%EE%B6%AF%D4%CB%D3%AA","%C9%CC%BC%D2%D4%CB%D3%AA","%C6%B7%C0%E0%D4%CB%D3%AA","%D3%CE%CF%B7%D4%CB%D3%AA","%CD%F8%C2%E7%CD%C6%B9%E3","%D4%CB%D3%AA%D7%A8%D4%B1","%CD%F8%B5%EA%D4%CB%D3%AA","%D0%C2%C3%BD%CC%E5%D4%CB%D3%AA","%BA%A3%CD%E2%D4%CB%D3%AA","%D4%CB%D3%AA%BE%AD%C0%ED","%B8%B1%D6%F7%B1%E0","%C4%DA%C8%DD%B1%E0%BC%AD","%CE%C4%B0%B8%B2%DF%BB%AE","%BC%C7%D5%DF","%CA%DB%C7%B0%D7%C9%D1%AF","%CA%DB%BA%F3%BF%CD%B7%FE","%CC%D4%B1%A6%BF%CD%B7%FE","%BF%CD%B7%FE%BE%AD%C0%ED","%D6%F7%B1%E0","%D4%CB%D3%AA%D7%DC%BC%E0","COO","%BF%CD%B7%FE%D7%DC%BC%E0","%CA%D0%B3%A1%B2%DF%BB%AE","%CA%D0%B3%A1%B9%CB%CE%CA","%CA%D0%B3%A1%D3%AA%CF%FA","%CA%D0%B3%A1%CD%C6%B9%E3","SEO","SEM","%C9%CC%CE%F1%C7%FE%B5%C0","%C9%CC%D2%B5%CA%FD%BE%DD%B7%D6%CE%F6","%BB%EE%B6%AF%B2%DF%BB%AE","%CD%F8%C2%E7%D3%AA%CF%FA","%BA%A3%CD%E2%CA%D0%B3%A1","%D5%FE%B8%AE%B9%D8%CF%B5","%C3%BD%BD%E9%BE%AD%C0%ED","%B9%E3%B8%E6%D0%AD%B5%F7","%C6%B7%C5%C6%B9%AB%B9%D8","%CF%FA%CA%DB%D7%A8%D4%B1","%CF%FA%CA%DB%BE%AD%C0%ED","%BF%CD%BB%A7%B4%FA%B1%ED","%B4%F3%BF%CD%BB%A7%B4%FA%B1%ED","BD%BE%AD%C0%ED","%C9%CC%CE%F1%C7%FE%B5%C0","%C7%FE%B5%C0%CF%FA%CA%DB","%B4%FA%C0%ED%C9%CC%CF%FA%CA%DB","%CF%FA%CA%DB%D6%FA%C0%ED","%B5%E7%BB%B0%CF%FA%CA%DB","%CF%FA%CA%DB%B9%CB%CE%CA","%C9%CC%C6%B7%BE%AD%C0%ED","%CA%D0%B3%A1%D7%DC%BC%E0","%CF%FA%CA%DB%D7%DC%BC%E0","%C9%CC%CE%F1%D7%DC%BC%E0","CMO","%B9%AB%B9%D8%D7%DC%BC%E0","%B2%C9%B9%BA%D7%DC%BC%E0","%CD%B6%D7%CA%D7%DC%BC%E0","%CE%EF%C1%F7","%B2%D6%B4%A2","%B2%C9%B9%BA%D7%A8%D4%B1","%B2%C9%B9%BA%BE%AD%C0%ED","%C9%CC%C6%B7%BE%AD%C0%ED","%B7%D6%CE%F6%CA%A6","%CD%B6%D7%CA%B9%CB%CE%CA","%CD%B6%D7%CA%BE%AD%C0%ED","%C8%CB%CA%C2/HR","%C5%E0%D1%B5%BE%AD%C0%ED","%D0%BD%D7%CA%B8%A3%C0%FB%BE%AD%C0%ED","%BC%A8%D0%A7%BF%BC%BA%CB%BE%AD%C0%ED","%C8%CB%C1%A6%D7%CA%D4%B4","%D5%D0%C6%B8","HRBP","%D4%B1%B9%A4%B9%D8%CF%B5","%D6%FA%C0%ED","%C7%B0%CC%A8","%D0%D0%D5%FE","%D7%DC%D6%FA","%CE%C4%C3%D8","%BB%E1%BC%C6","%B3%F6%C4%C9","%B2%C6%CE%F1","%BD%E1%CB%E3","%CB%B0%CE%F1","%C9%F3%BC%C6","%B7%E7%BF%D8","%D0%D0%D5%FE%D7%DC%BC%E0/%BE%AD%C0%ED","%B2%C6%CE%F1%D7%DC%BC%E0/%BE%AD%C0%ED","HRD/HRM","CFO","CEO","%B7%A8%CE%F1","%C2%C9%CA%A6","%D7%A8%C0%FB","%CD%B6%D7%CA%BE%AD%C0%ED","%B7%D6%CE%F6%CA%A6","%CD%B6%D7%CA%D6%FA%C0%ED","%C8%DA%D7%CA","%B2%A2%B9%BA","%D0%D0%D2%B5%D1%D0%BE%BF","%CD%B6%D7%CA%D5%DF%B9%D8%CF%B5","%D7%CA%B2%FA%B9%DC%C0%ED","%C0%ED%B2%C6%B9%CB%CE%CA","%BD%BB%D2%D7%D4%B1","%B7%E7%BF%D8","%D7%CA%D0%C5%C6%C0%B9%C0","%BA%CF%B9%E6%BB%FC%B2%E9","%C2%C9%CA%A6","%C9%F3%BC%C6","%B7%A8%CE%F1","%BB%E1%BC%C6","%C7%E5%CB%E3","%CD%B6%D7%CA%D7%DC%BC%E0","%C8%DA%D7%CA%D7%DC%BC%E0","%B2%A2%B9%BA%D7%DC%BC%E0","%B7%E7%BF%D8%D7%DC%BC%E0","%B8%B1%D7%DC%B2%C3"]
cate_queue = Queue.Queue()
exist_queue = []
proxies_pool = Queue.Queue()

class Crawer(threading.Thread):
	def __init__(self,filename,tid,proxies_s,lock):
		threading.Thread.__init__(self)
		# self.url = url
		self.filename=filename
		self.tid=tid
		self.proxies={"http":proxies_s}
		self.lock = lock
		print str(self.tid)+' is start  当前使用代理ip'.decode('utf-8').encode('gbk')+str(self.proxies)
	def run(self):
		# global g_mutex
		global cate_queue
		global exist_queue
		_cookies = self.getCookie()
		_headers = self.GetHea()
		while(cate_queue.qsize()>0):
			print 'running  &********************&'
			sleep(2)
			try:
				url = cate_queue.get(block=False)
			except Exception:
				break
			Html_Info = self.GetUrlInfo(url,_headers,_cookies)
			if Html_Info:
				return_info = self.write(self.filename,Html_Info)
				# print 'html info  &********************&'
				if return_info:
					self.lock.acquire()
					f=open('exists_url.txt',"a+")
					f.write(str(url)+'\n')
					f.close()
					self.lock.release()
				else:
					print 'error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'

			else:
				return False
		# return False

	def GetUrlInfo(self,url,h,c):
		global cate_queue
		try:
			sleep(1)
			_Info = requests.get(url,headers=h,cookies=c,proxies=self.proxies,timeout=10).content
			print str(len(json.loads(_Info)["content"]["positionResult"]["result"]))+'  result  changdu'
			print "**************************"
			if len(json.loads(_Info)["content"]["positionResult"]["result"]):
				# print len(json.loads(_Info)["content"]["positionResult"]["result"])
				
				return _Info
			else:
				cate_queue.queue.clear()
				print len(json.loads(_Info)["content"]["positionResult"]["result"])
				# proxies_pool.queue.clear()
				return False
		except Exception:
			print Exception
			print self.proxies
			self.change_proxies()
			return self.GetUrlInfo(url,h,c)
			print 'getUrl错误了哦    '.decode('utf-8').encode('gbk')+str(self.proxies)



	def change_proxies(self):
		global proxies_pool
		print str(proxies_pool.qsize())+' number of proxies_pool'
		if proxies_pool.qsize()>0:
			# try:
			print str(self.tid)+str(self.proxies)+' 改变当前使用代理ip'.decode('utf-8').encode('gbk')
			self.proxies={"http":proxies_pool.get().replace('\r\n','')}
		else:
			return 
	def GetHea(self):
		header_s = [
		           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
		          
		]
		return random.choice(header_s)
	def getCookie(self):
		cookiess = {"user_trace_token":"20160615180157-31f44a23-32e0-11e6-850a-525400f775ce","LGUID":"20160615180157-31f44eff-32e0-11e6-850a-525400f775ce","LGMOID":"20160818230933-22A722E63328C33922CD6F303E1E94DE","index_location_city":"%E5%85%A8%E5%9B%BD","HISTORY_POSITION":"2173299%2C10k-20k%2C%E5%A6%99%E8%AE%A1%E6%97%85%E8%A1%8C%2C%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86%7C692153%2C3k-6k%2COpenCom%2C%E6%B5%8B%E8%AF%95%E5%B7%A5%E7%A8%8B%E5%B8%88%7C2086516%2C8k-10k%2C%E7%A7%9F%E7%A7%9F%E8%BD%A6%2C%E6%B5%8B%E8%AF%95%E5%B7%A5%E7%A8%8B%E5%B8%88%7C","SEARCH_ID":"26ea5992a2e74c38af93ad0858911228","ctk":"1472535876","JSESSIONID":"AC2C720AC0983E8D9D4BD8A617ECD146"}
		return cookiess 
	def write(self,filename,message):
		# global g_mutex
		self.lock.acquire()
		f = open(filename+'.txt',"a+")
		f.write(message+'\n')
		f.close()
		self.lock.release()
		return True

# def getURL
def GetUrls(category_name):
	sleep(2)
	print category_name.decode('utf-8').encode('gbk')
	global proxies_pool
	# replace
	url = 'http://www.lagou.com/jobs/positionAjax.json?px=new&kd='+str(category_name)+'&pn=1'
	print url.decode('utf-8').encode('gbk')

	_proxies = {'http':proxies_pool.get(block=False).replace('\r\n','')}
	print _proxies

	cookiesss = {"user_trace_token":"20160615180157-31f44a23-32e0-11e6-850a-525400f775ce","LGUID":"20160615180157-31f44eff-32e0-11e6-850a-525400f775ce","LGMOID":"20160818230933-22A722E63328C33922CD6F303E1E94DE","index_location_city":"%E5%85%A8%E5%9B%BD","HISTORY_POSITION":"2173299%2C10k-20k%2C%E5%A6%99%E8%AE%A1%E6%97%85%E8%A1%8C%2C%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86%7C692153%2C3k-6k%2COpenCom%2C%E6%B5%8B%E8%AF%95%E5%B7%A5%E7%A8%8B%E5%B8%88%7C2086516%2C8k-10k%2C%E7%A7%9F%E7%A7%9F%E8%BD%A6%2C%E6%B5%8B%E8%AF%95%E5%B7%A5%E7%A8%8B%E5%B8%88%7C","SEARCH_ID":"26ea5992a2e74c38af93ad0858911228","ctk":"1472535876","JSESSIONID":"AC2C720AC0983E8D9D4BD8A617ECD146"}
	# size_s=
	try:
		r = requests.get(url,proxies=_proxies,cookies=cookiesss,timeout=10)
		counts = json.loads(r.content)
		size_s = int(counts['content']['positionResult']['totalCount'])
		print size_s
		return size_s

	except Exception:
		print 'use  error  way'
		return GetUrls(category_name)	
	# return size_s
	# return False
	

if __name__ == '__main__':


	# global cate_queue
	for d in xrange(0,len(GangWeiLists)):

		# proxies_pool.queue.clear()
 		f = open("kuaiOK.txt",'r')
		for line in f:
			if line !='':
				proxies_pool.put(line)	
		print proxies_pool.qsize()
		f=open('error.txt','a+')
		sizess = GetUrls(GangWeiLists[d])
		print sizess
		a  = int(sizess)/15


		if int(a)>600:
			f.write(str(GangWeiLists[d])+'   is 600'+'\r\n')
			a=600
		threads=[]
		if int(sizess)>int(200000):
			# f=open('error.txt','a+')
			f.write(str(GangWeiLists[d])+'\r\n')
		
		else:
			for i in xrange(1,a+1):
				cate_queue.put('http://www.lagou.com/jobs/positionAjax.json?px=new&kd=%s&pn=%d'%(GangWeiLists[d],int(i)))
				print i
			print cate_queue.qsize()
			for c in xrange(6):
				threads.append(Crawer(GangWeiLists[d].replace('/','-').decode('utf-8').encode('gbk'),c,proxies_pool.get(block=False).replace('\r\n',''),g_mutex))
			for x in threads:
				x.start()
			for x in threads:
				x.join()
		f.close()
		
	# print proxies_pool.get()






