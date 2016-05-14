# coding=utf-8
import urllib
import urllib2
import re
import  thread
import time
import codecs

class QSBK:

    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        self.headers = {'User-Agent' :self.user_agent}
        self.stories = []
        self.enable = False
        self.file = codecs.open('/Users/sunkun/Desktop/joke.txt','a','utf-8')
        self.count = 1

    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
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
        pattern = re.compile('h2>(.*?)</h2.*?content">(.*?)</.*?number">(.*?)</', re.S)
        pageCode = re.sub(r'<br[ ]?/?>', '\n  ', pageCode)
        items = re.findall(pattern,pageCode)
        pageStories = []
        for item in items:
            pageStories.append([item[0].strip(),item[1].strip(),item[2].strip()])

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

            self.loadPage()

            str = u"----------孙琨:祝大家笑口常开,开心每一天😄---------\n" \
                  u"【段子】 %d / 100\n" \
                  u"【发布人】%s\n" \
                  u"【点赞】%s\n" \
                  u"【内容】\n" \
                  u"  %s\n\n" % (self.count, story[0], story[2], story[1])
            self.file.write(str)
            self.count += 1
            print u"success \n第%d页\t发布人: %s\t 赞: %s\n%s\n\n" % (page, story[0], story[2], story[1])

            if self.count == 101:
                self.enable = False
                return
       # for story in pageStories:
            #input = raw_input()
           # self.loadPage()
           # if input == "Q":
           #     self.enable = False
           #     return
        #    print u"第%d页\t发布人：%s\t 赞：%s\n%s" %(page,story[0],story[2],story[1])

    def start(self):
        print u'正在读取。。。。'
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                pageStories = self.stories[0]
                nowPage +=1
                del self.stories[0]
                self.getOneStory(pageStories,nowPage)

spider = QSBK()
spider.start()
