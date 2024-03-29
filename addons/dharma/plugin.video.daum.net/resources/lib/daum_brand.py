# -*- coding: utf-8 -*-
"""
  Best video clip
"""
import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re

class DaumBrand:
  menu_list = []
  video_list = []
  nextpage = None
  def DaumBrand(self):
    pass

  def parseTop(self,url):
    link = urllib.urlopen(url)
    soup = BeautifulSoup( link.read(), fromEncoding="utf-8" )
    self.menu_list = []
    #-- item list
    strain1 = SoupStrainer( "div", { "class" : "programList" } )
    strain2 = SoupStrainer( "div", { "class" : "listBody" } )
    for item in soup.find(strain1).find(strain2).findAll('li'):
      url = item.a['href'].replace("&amp;","&")
      url = "http://tvpot.daum.net"+url
      title = item.a.string
      title = title.replace("&lt;","<").replace("&gt;",">").replace("&amp;","&")
      self.menu_list.append( (title,url) )

  def parse(self,main_url):
    link = urllib.urlopen(main_url)
    soup = BeautifulSoup( link.read(), fromEncoding="utf-8" )
    self.video_list = []
    self.nextpage = None
    base_url = main_url[:main_url.rfind('/')+1]
    #-- item list
    strain = SoupStrainer( "div", { "class" : re.compile("^listBody") } )
    items = soup.find(strain).findAll('dl')
    for item in items:
      ddimg = item.find('dd',{'class' : 'image'})
      ref = ddimg.find('a')
      if ref is None:
        continue
      vid_url = ref['href'].replace("&amp;","&")
      vid_url = vid_url.replace("&amp;","&").replace(" ","")
      if vid_url[0] == '/':
        vid_url = "http://tvpot.daum.net"+vid_url
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
      title = title.replace("&lt;","<").replace("&gt;",">").replace("&amp;","&")
      self.video_list.append( (title,vid_url,thumb) )
    #-- next page
    sect = soup.find("table", {"class" : "pageNav2"})
    if sect:
      nextpg = sect.find('span', {"class" : "sel"}).parent.findNextSibling('td')
      if nextpg:
        url = nextpg.a['href'].replace("&amp;","&")
        if url.startswith("http"):
          pass
        elif url.startswith("/"):
          url = "http://tvpot.daum.net"+url
        else:
          url = base_url + url
        self.nextpage = url

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
