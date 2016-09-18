#coding:utf-8
#包封装格式
#pack('<llhbb%ds' % (8), 4, 4, 8, 0, 0, 'hahahaha' + '\0')
# 两个四字节
#一个二字节(消息类型)
#两个一字节(加密字段  保留字段)  末尾要\0结束
from struct import pack, unpack
import socket,re,threading,requests,time
MESSAGE_TYPE_FROM_CLIENT = 689
timeout = 20
socket.setdefaulttimeout(timeout)
class danmu(object):
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.rid = 71017
		self.gid = -9999
	def ConnectDanMuServer(self):
		HOST = 'openbarrage.douyutv.com'
		PORT=8601
		# self.log("连接弹幕服务器..."+HOST+':'+str(PORT))
		self.sock.connect((HOST, PORT))
		print "连接成功,发送登录请求...".decode('utf-8').encode('gbk')
		# pass
	def KeepLive(self):
		while True:
			
			self.SendMsg(self.Pack('type@=keeplive/tick@='+str(int(time.time()))+'/'))
			print self.Pack('type@=keeplive/tick@='+str(int(time.time()))+'/')
			print '----------------------keeplive is send-----------------------'
			data = self.sock.recv(1024)
			print 'Received'+repr(data)
			time.sleep(20)
			# time.sleep(25)


	def GetInfo():
		pass

	def Main(self):
		self.ConnectDanMuServer()
		self.LoginReq()
		self.JoinGroup()
		threading.Thread(target=danmu.KeepLive,args=(self,)).start()
		self.console_msg()
		
	def Pack(self,msg):
		raw_num = len(msg)+9
		#两个四字节的消息长度
		#1个结尾的\0
		head = pack('<llhbb%ds' % (len(msg)+1), raw_num, raw_num, MESSAGE_TYPE_FROM_CLIENT, 0, 0, msg+ '\x00')
		# print head
		#数据报封装方式
		return head
	def SendMsg(self,packet):
		self.sock.send(packet)
	def console_msg(self):
		while True:
			data = self.sock.recv(1024)
			self.ChuliReturnMsg(self.UnPack(data))
	def LoginReq(self):

		msg = 'type@=loginreq/roomid@='+str(self.rid)+'/'
		self.SendMsg(self.Pack(msg))
	def LoginOut(self):
		msg='type@=logout/'
		self.SendMsg(self.Pack(msg))
	def JoinGroup(self):
		msg='type@=joingroup/rid@='+str(self.rid)+'/gid@='+str(self.gid)+'/'
		self.SendMsg(self.Pack(msg))

	def UnPack(self,msg):
		#消息长度msg_len
		#消息类型
		#加密字段
		#保留字段
		#数据部分
		buff_len = len(msg)
		if buff_len<12:
			# self.LoginOut()
			return None
		packet_length_1, packet_length_2, msg_type, encryption, reserved, body = unpack('<llhbb%ds' % (buff_len - 12), msg)
		return body
	def ChuliReturnMsg(self,msg):
		try:
			msg_type = re.search(b'type@=(\w*)', msg)
		except TypeError:
			msg_type = re.search('type@=(\w*)', str(msg))
		# print msg

		if msg_type:
			if msg_type.group(1)=='chatmsg':
				try:
					danmu = re.search(b'nn@=(.*?)/txt@=(.*?)/',msg)
				except Exception:
					danmu = re.search('nn@=(.*?)/txt@=(.*?)/',str(msg))
				# print(data)
					                    
				try:
				# self.log(danmu.group(1).decode()+'\t:\t'+danmu.group(2).decode())
					self.log('success',msg)
					print danmu.group(1).decode('utf-8').encode('gbk')+"  :  "+danmu.group(2).decode('utf-8').encode('gbk')
				except BaseException as e:
					self.log('error',str(msg))
					print "\t\t_________解析弹幕信息失败:".decode('utf-8').encode('gbk')+str(msg)
		else:
			# print msg
			pass
	def log(self,filename,msg):
		f = open(str(filename)+'.txt','a+')
		f.write(msg+'\n')
		f.close()
if __name__ == '__main__':
	a = danmu()
	a.Main()