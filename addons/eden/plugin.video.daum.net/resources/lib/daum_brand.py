# -*- coding: utf-8 -*-
"""
  Best video clip
"""
import urllib
from BeautifulSoup import BeautifulSoup
import re

class DaumBrand:
  root_url = "http://tvpot.daum.net"
  menu_list = []
  video_list = []
  prevpage = None
  nextpage = None
  def DaumBrand(self):
    pass

  @staticmethod
  def getList(url):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup( html, fromEncoding="utf-8", convertEntities=BeautifulSoup.HTML_ENTITIES )
    brand_list = []
    #-- item list
    sec = soup.find("div",{"class":"brandMap"}).find("div",{"class":"mapContents"})
    for grp in soup.findAll("h4"):
      gout = { 'list':[] }
      gout['title'] = grp.string
      for item in grp.findNextSibling('ul').findAll('a'):
        brand_id = re.compile('ownerid=(.*)').search(item['href']).group(1)
        title = item.string
        gout['list'].append( (title,brand_id) )
      brand_list.append( gout )
    return brand_list

  @staticmethod
  def getList2(url):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup( html, fromEncoding="utf-8", convertEntities=BeautifulSoup.HTML_ENTITIES )
    brand_list = []
    #-- item list
    for section in soup.findAll("div", {"class":re.compile("^cate_")}):
      gout = {'list':[]}
      gout['title'] = section.find('h4').string
      for item in section.findAll('a'):
        brand_id = re.compile('ownerid=(.*)').search(item['href']).group(1)
        title = item.string
        gout['list'].append( (title,brand_id) )
      brand_list.append( gout )
    return brand_list

  def parseTop(self,url):
    link = urllib.urlopen(url)
    soup = BeautifulSoup( link.read(), fromEncoding="utf-8", convertEntities=BeautifulSoup.HTML_ENTITIES )
    base_url = url[:url.rfind('/')+1]
    #-- item list
    sec = soup.find("div",{"class":"programList"}).find("div",{"class":"listBody"})
    self.menu_list = []
    for grp in sec.findAll("ul"):
      gout = { 'list':[] }
      # group name
      item = grp.findPreviousSibling('h3')
      if item:
      	gout['name'] = item.string
      # program list
      for item in grp.findAll("li"):
        url = self.translate_url(item.a['href'], base_url)
        title = item.a.string
        gout['list'].append( (title,url) )
      self.menu_list.append( gout )

  def parse(self,main_url):
    link = urllib.urlopen(main_url)
    soup = BeautifulSoup( link.read(), fromEncoding="utf-8" )
    self.video_list = []
    self.prevpage = None
    self.nextpage = None
    base_url = main_url[:main_url.rfind('/')+1]
    #-- item list
    sec = soup.find("div", {"class":re.compile("^listBody")})
    for item in sec.findAll('dl'):
      ddimg = item.find('dd',{'class' : 'image'})
      ref = ddimg.find('a')
      if ref is None:
        continue
      vid_url = self.translate_url(ref['href'].replace(' ',''), base_url)
      imgpt = ddimg.find('img')
      thumb = imgpt['src']

      if ref.has_key('title'):
        title = ref['title']
      elif imgpt.has_key('title'):
        title = imgpt['title']
      elif imgpt.has_key('alt'):
        title = imgpt['alt']
      else:
        title = "Unknown"
      query = re.compile(u"동영상 '(.*?)'의 미리보기 이미지").match(title)
      if query:
        title = query.group(1)
      self.video_list.append( (title,vid_url,thumb) )
    #-- page navigation
    sect = soup.find("table", {"class" : "pageNav2"})
    if sect:
      curpg = sect.find('span', {"class" : "sel"}).parent
      prevpg = curpg.findPreviousSibling('td')
      if prevpg:
        self.prevpage = self.translate_url(prevpg.a['href'], base_url)
      nextpg = curpg.findNextSibling('td')
      if nextpg:
        self.nextpage = self.translate_url(nextpg.a['href'], base_url)

  def translate_url(self,url,base_url):
      url = url.replace('&amp;','&')
      if url.startswith("http"):
        pass
      elif url.startswith("/"):
        url = self.root_url + url
      else:
        url = base_url + url
      return url

if __name__ == "__main__":
  site = DaumBrand()
  site.parseTop("http://tvpot.daum.net/brand/ProgramView.do?ownerid=O_5rgf7M1do0&playlistid=1101578&page=1")
  print len(site.menu_list)
  print site.menu_list[0]

  site.parse("http://tvpot.daum.net/brand/ProgramView.do?ownerid=O_5rgf7M1do0&playlistid=1101578&page=2&viewtype=24")
  print len(site.video_list)
  print site.video_list[0]
  print site.nextpage

  site.parse("http://tvpot.daum.net/brand/ProgramView.do?page=4&ownerid=hZu8dgCZmzQ0&playlistid=78324&viewtype=14")
  print len(site.video_list)
  print site.video_list[0]
  print site.nextpage
# vim: softtabstop=2 shiftwidth=2 expandtab
