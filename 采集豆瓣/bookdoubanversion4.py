# -*- coding:UTF-8 -*-
#Author:周文康
import time
import requests
import sys
from bs4 import BeautifulSoup
from time import ctime,sleep
import threading
import Queue
import random
import codecs
import json
import multiprocessing
start = time.clock()
reload(sys)
sys.setdefaultencoding('utf-8')




####有的page居然要检验referer  我也是醉了  不然就302
###再改进一点
#listss = ["小说","日本","历史","外国文学","漫画","文学","中国","心理学","随笔","哲学","绘本","中国文学","推理","美国","爱情","经典","传记","日本文学","散文","青春","文化","旅行","社会学","英国","言情","科幻","科普","村上春树","生活","东野圭吾","艺术","台湾","悬疑","设计","经济学","成长","管理","励志","法国","武侠","政治","社会","奇幻","心理","经济","思维","韩寒","诗歌","童话","日本漫画","摄影","建筑","耽美","亦舒","金融","商业","女性","宗教","杂文","电影","王小波","互联网","三毛","人生","儿童文学","古典文学","计算机","英国文学","数学","安妮宝贝","张爱玲","网络小说","投资","职场","香港","政治学","名著","余华","推理小说","美国文学","美食","郭敬明","教育","穿越","金庸","德国","游记","轻小说","工具书","回忆录","人类学","个人管理","编程","思想","纪实","教材","营销","英语","阿加莎·克里斯蒂","中国历史","几米","国学","東野圭吾","时间管理","灵修","BL","散文随笔","心灵","政治哲学","魔幻","法国文学","张小娴","音乐","幾米","人性","青春文学","当代文学","哈利波特","人文","科学"]




class Message:
    def __init__(self,book_link,name,book_image,book_info,content,booktags,star_dicts,rate_num,rate_peo):
        self.book_link=book_link
        self.name=name
        self.book_image=book_image
        self.book_info = book_info
        self.content=content
        self.booktags=booktags
        self.star_dicts=star_dicts
        self.rate_num=rate_num
        self.rate_peo=rate_peo
        print self.book_link
    def packdd(self):
        try:
            print self.name
        except Exception:
            print 'this is error but it is ok'
        dicts = {}
        dicts["book_link"] = self.book_link
        dicts["book_name"]=self.name
        dicts["book_image"]=self.book_image
        dicts["book_info"]=self.book_info
        dicts["content_intro"]=self.content
        dicts["book_tags"]=self.booktags
        dicts["rate"]={}
        dicts["rate"]['rate_num']=self.rate_num
        dicts["rate"]['rate_peo']=self.rate_peo
        dicts["rate"]['rate_star']=self.star_dicts
        # print dicts
        return dicts

#信息返回格式
#{"bookname":"xxx","book_image":"xxxx","content_intro":"xxx","booktags":"xxx","rate":{"rate_num":"xxx","rate_peo":"xxx","rate_star":{"star_five":"xxx","star_four":"xxx","star_three":"xxx","star_two":"xxx","star_one":"xxx"}}}



def getHtmlInfo(urls,ref):

    global _cookies
    global starts
    #简单获取
    starts = time.clock()
    headers = [
           {'User-Agent': 'Mozilla/6.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
           {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
           {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
           {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
           {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
    ]
    # url = u'https://book.douban.com/subject/'+str(ids)
    # sleep(1)

    try:
        header = random.choice(headers)
        header['Referer']= ref
        ContentPage_Info = requests.get(urls,headers=header,cookies=_cookies)
    except Exception:
        header = random.choice(headers)
        header['Referer']= ref
        ContentPage_Info = requests.get(urls,headers=header,cookies=_cookies)
    if (ContentPage_Info.status_code==403):
        sleep(30)
        _cookies = requests.get('https://book.douban.com').cookies
        print ContentPage_Info.status_code
        getHtmlInfo(urls,ref)
    # sleep(1)
    print ContentPage_Info.status_code
    print queues.qsize()
    ends = time.clock()
    #计算网页获取速度处理
    print 'GetPage time: %s Seconds'%(ends-starts)
    return ContentPage_Info

    
def HandleInfo(Book_Url,ContentPage_Info):
    Page_Html = BeautifulSoup(ContentPage_Info.content)
    #bookname
    try:
        bookname = Page_Html.title.string
    finally:
        bookname = Page_Html.title.string
    #bookimage
    try:
        book_image = Page_Html.select('#mainpic > a')[0].attrs['href']
    except Exception:
        book_image=''

    try:
        book_info = Page_Html.select("#info")[0].get_text().replace('-',':').replace(' ','').replace('\n','-').replace('---','').replace('--','-')
        booktags = Page_Html.select('#db-tags-section .indent > span')
    except Exception:
        if str(ContentPage_Info.history[0]) =="<Response [302]>":
            book_info=''
            booktags=''
        else:
            book_info='无'
            booktags='无'
    bookt = []
    for i in xrange(len(booktags)):
        bookt.append(booktags[i].get_text().replace(' ','').replace('\n','').replace(u'\xa0',u''))
    booktags = ','.join(bookt)
    # 书本标签    


    try:
        #评分人数
          rate_peo = Page_Html.select('#interest_sectl > div > div > strong')[0].get_text() 
          #评分
          rate_num= Page_Html.select('#interest_sectl .rating_sum > span > a > span')[0].get_text()
          Page_Htmls = Page_Html.find('div',id='interest_sectl')
          Star_Info  = Page_Htmls.find_all("span")
          star_list=[u'star_five',u'star_four',u'star_three',u'star_two',u'star_one']
          rate_list=[]
          for i in xrange(3,len(Star_Info)):
              if not i%2:
                  rate_list.append(Star_Info[i].get_text().replace('\n','').replace(' ',''))
              # 星星 
          # print star_list
          # print rate_list
          dicts = zip(star_list,rate_list)
    except Exception:
          try:
              rate_peo=Page_Html.select('.rating_sum > span > a ')[0].get_text()
              rate_num=rate_peo
              dicts = {'rate_msg':rate_peo}
          except Exception:
              rate_peo='评价人数不足'
              rate_num=rate_peo
              dicts = {'rate_msg':rate_peo}
    try:
        content = Page_Html.select('#link-report > div .intro')[0].get_text().replace('\n','')
    except IndexError:
        try:
            content=Page_Html.select('.intro')[0].get_text().replace('\n','')
        except Exception:
            content=''
    #书本简要描述

    aa = Message(Book_Url,bookname,book_image,book_info,content,booktags,dicts,rate_num,rate_peo)
    ccc = aa.packdd()
    ends = time.clock()
        #计算网页获取速度处理
    print 'controlPage time: %s Seconds'%(ends-starts)
    return ccc


#拼凑出分页所需要的url
def makeUrl(Ref_url,values):
    url = str(Ref_url)+'?start='+str((values*20))+'&type=T'
    # print url
    print url.decode('utf-8').encode('gbk')
    return url

def getPage(url):
    sss = requests.Session()
    header_ss = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    header_ss['Referer']='https://book.douban.com/'
    dddd = sss.get(url,headers = header_ss)
    ccc = BeautifulSoup(dddd.content)
    print ccc
    value_s = ccc.select('#subject_list .paginator > a')
    return int(value_s[-1].get_text())
#得到分类内所有的url
def getUrl(pops_url):
    # print pops_url
    print 'start'
    global queues
    aaa = getPage(pops_url)
    t=0
    while t < 1:
        for z in xrange(int(aaa)):
            # sleep(1)
            urls = makeUrl(pops_url,z)
            a = getUrls(urls)
            if a:
                for i in xrange(0,len(a)):
                    queues.put(a[i].attrs['href'])
            else:
                break
            print queues.qsize()
        t+=1
    return 

def getUrls(url):
    global _cookies
    header_s = [
           {'User-Agent': 'Mozilla/6.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
           {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
           {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
           {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
           {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
           {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
    ]
    # print url
    try:
        header = random.choice(header_s)
        header["Referer"]='https://book.douban.com/tag/?view=type'
        sleep(1)
        r=requests.get(url,headers=header,cookies=_cookies)
    except Exception:
        header = random.choice(header_s)
        header["Referer"]='https://book.douban.com/tag/?view=type'
        r=requests.get(url,headers=header,cookies=_cookies)
    else:
        header = random.choice(header_s)
        header["Referer"]='https://book.douban.com/tag/?view=type'
        r=requests.get(url,headers=header,cookies=_cookies)
    soup =BeautifulSoup(r.content)
    # print r.content
    if soup.select('.info') !='[]':
        infourl = soup.select('.info > h2 > a')
    else:
        return False
    if(r.status_code==403):
        print r.status_code
        sleep(30)
        # print '123'
        _cookies = requests.get('https://book.douban.com').cookies
        print url.decode('utf-8').encode('gbk')
        getUrls(url)
    return infourl


def pop(strring):
    return 'https://book.douban.com/tag/'+str(strring)
def aaa(Ref_Url,filename):
    # sleep(5)
    global starts
    global queues
    # global filename
    
    while(queues.qsize()>0):
        Url_Page = queues.get()
        ffff = HandleInfo(Url_Page,getHtmlInfo(Url_Page,Ref_Url))
        f = open(filename.decode('utf-8').encode('gbk')+'.txt','a+')
        f.write(json.dumps(ffff,ensure_ascii=False)+'\n')
        f.close()
        ends = time.clock()
        #计算网页获取速度处理
        print 'OnePage time: %s Seconds'%(ends-starts)

# url = 'https://book.douban.com/subject/4031698/'
# HandleInfo(url,getHtmlInfo(url,''))
queues = Queue.Queue()


_cookies = requests.get('https://book.douban.com').cookies

def main(mul_que):
        # global mul_que
        while mul_que.qsize>0:
            filename = mul_que.get()
            RRREEEFFF = pop(str(filename))
            getUrl(RRREEEFFF)
            aaa(RRREEEFFF,filename)
        return False

if __name__ == '__main__':
        mul_que = multiprocessing.Queue()
        listss = ["爱情","经典","传记","日本文学","散文","青春","文化","旅行","社会学","英国","言情","科幻","科普","村上春树","生活","东野圭吾","艺术","台湾","悬疑","设计","经济学","成长","管理","励志","法国","武侠","政治","社会","奇幻","心理","经济","思维","韩寒","诗歌","童话","日本漫画","摄影","建筑","耽美","亦舒","金融","商业","女性","宗教","杂文","电影","王小波","互联网","三毛","人生","儿童文学","古典文学","计算机","英国文学","数学","安妮宝贝","张爱玲","网络小说","投资","职场","香港","政治学","名著","余华","推理小说","美国文学","美食","郭敬明","教育","穿越","金庸","德国","游记","轻小说","工具书","回忆录","人类学","个人管理","编程","思想","纪实","教材","营销","英语","阿加莎·克里斯蒂","中国历史","几米","国学","東野圭吾","时间管理","灵修","BL","散文随笔","心灵","政治哲学","魔幻","法国文学","张小娴","音乐","幾米","人性","青春文学","当代文学","哈利波特","人文","科学"]
        for i in listss:
                print i 
                mul_que.put(i)
        prcc = []
        for i in xrange(20):
            prcc.append(multiprocessing.Process(target=main, args=(mul_que,)))
        for i in prcc:
            i.start()
            sleep(2)
        for i in prcc:
            i.join()
        end = time.clock()
        print 'Running time: %s Seconds'%(end-start)
    # print getPage('https://book.douban.com/tag/%E6%9D%91%E4%B8%8A%E6%98%A5%E6%A0%91?start=0&type=T')

# print header
