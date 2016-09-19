filename = str(raw_input('请输入要去重行数的'.decode('utf-8').encode('gbk')))
a = set([x for x in open(filename+".txt",'r').readlines() if x.strip()!=''])

f = open('well.txt','a+')
for i in xrange(len(a)):
	f.write(list(a)[i])
f.close()