# coding=utf-8
import urllib
import urllib2
import re
import  thread
import time

class Liepin:

    def __init__(self):
        self.pageIndex = 1
        self.user_agent = ''
        self.headers = {'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
        self.stories = []
        self.enable = False

    def getPage(self,pageIndex):
        try:
            url = 'https://www.liepin.com/zhaopin/?industries=&dqs=&salary=&jobKind=&pubTime=&compkind=&compscale=&industryType=&searchType=1&clean_condition=&isAnalysis=&init=1&sortFlag=15&flushckid=0&fromSearchBtn=1&headckid=18c5e8ff61ff95c6&d_headId=e6fa66610039683b7cf244de1664fe08&d_ckId=e6fa66610039683b7cf244de1664fe08&d_sfrom=search_fp&d_curPage=0&d_pageSize=40&siTag=iitW4pPueI8QV60jbgZVng~fA9rXquZc5IkJpXC-Ycixw&key=%E8%AE%A1%E7%AE%97%E6%9C%BA%E5%B7%A5%E7%A8%8B%E5%B8%88' + str(pageIndex)
            request = urllib2.Request(url,headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print "error",e.reason
                return None

    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "page load error"
            return None
        pattern = re.compile('<div class="job-info">.*?<a.*?>(.*?)</a>.*?<span class="text-warning">(.*?)</span>.*?<a.*?>(.*?)</a>.*?<p class="company-name">.*?<a.*?>(.*?)</a>',re.S)
        items = re.findall(pattern,pageCode)
        pageStories = []
        for item in items:
            pageStories.append([item[0].strip(),item[1].strip(),item[2].strip(),item[3].strip()])
        return pageStories

    def loadPage(self):
        if self.enable==True:
            if len(self.stories)<2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex +=1

    def getOneStory(self,pageStories,page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            print u"\t职位：%s  \t公司：%s  \n地点：%s  \t工资：%s" %(story[0],story[3],story[2],story[1])

    def start(self):
        print u'正在读取，回车查看，Q退出'
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                pageStories = self.stories[0]
                nowPage +=1
                del self.stories[0]
                self.getOneStory(pageStories,nowPage)

spider = Liepin()
spider.start()
