﻿# -*- coding: utf-8 -*-
"""
  Retrieve medata for TV series from Daum
"""

import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer, NavigableString
import re
from meta_series import SeriesMetaData

class SeriesFetcher:
	type = "series"
	site = "Daum"
	meta = None

	EpisodeFound = False
	Season = 1;
	last_epnum = 0;

	def __init__(self): 
		self.base_url	= "http://movie.daum.net"
		self.search_url  = self.base_url+"/search.do?type=tv&q=%s"
		self.details_url = self.base_url+"/tv/detail/main.do?tvProgramId=%s"
		self.cast_url	= self.base_url+"/tv/detail/castcrew.do?tvProgramId=%s"
		self.photo_url   = self.base_url+"/tv/detail/photo/list.do?tvProgramId=%s&order=recommend"
		self.episode_base_url = self.base_url+"/tv/detail/episode.do"
		self.episode_url = self.episode_base_url+"?tvProgramId=%s"
		self.striptags = re.compile('<.*?>',re.U)
		self.meta = SeriesMetaData()

	# search with title
	def Search(self,title): 
		resp = urllib.urlopen( self.search_url % urllib.quote_plus(title.encode('utf-8')) );
		print self.search_url % urllib.quote_plus(title.encode('utf-8'))
		soup = BeautifulSoup(resp.read(),fromEncoding="utf-8")
		result = []
		for item in soup.findAll("span",{"class" : "fl srch"}):
			id = re.compile("tvProgramId=(\d+)").search(item.find('a')['href']).group(1)
			if item.a.b is None:
				title = item.a.string
			else:
				title = item.a.b.string
			result.append( (id,title) )
		return result

	def ParseSeriesPage(self,id):
		resp = urllib.urlopen( self.details_url % id );
		soup = BeautifulSoup(resp.read(),fromEncoding="utf-8")

		strain = SoupStrainer("div",{"id" : "tvInfoDetail"})
		header = soup.find(strain).find("p",{"class":"header"})
		self.meta.s_title = header.strong.string		# class=title_kor
		Season = 1
		#query = re.compile(u"^(.*)\s+시즌 (\d+)$").find(self.meta.s_title)
		#if query:
		#	self.meta.s_title = query.group(1)
		#	Season = int(query.group(2))
		self.meta.s_year = header.em.string[1:-1]
		aka = header.find("em",{"class":"title_AKA"})
		temp = aka.find("span",{"class":"eng"})
		if temp:
			self.meta.s_aka = temp.string
		else:
			self.meta.s_aka = aka.contents and aka.contents[0]

		self.meta.s_genres = []
		sect = soup.find("dl",{"class":"cu mainInfo"}).find("span",{"class" : "baseinfo"})
		pts = self.striptags.sub('',sect.renderContents()).split('|')
		self.meta.s_network = pts[0].strip()

		self.meta.s_rating = float( soup.find("span",{"class":"star_big pink"}).em.string )
		self.meta.s_poster = re.compile('C\d{3}x\d{3}').sub('image', soup.find('p', {"class" : "poster"}).a.img['src'])
		self.meta.s_plot = self.striptags.sub('', soup.find("div",{"id":"synopsis"}).find("div",{"class":"txt"}).renderContents()).strip()
		self.meta.s_plot = unicode(self.meta.s_plot.replace("&#39;","'"),'utf-8')

		self.meta.s_id = id
		self.meta.s_directors = []
		self.meta.s_writers = []
		self.meta.s_actors = []
		self.meta.s_backdrop_list = []

		self.ParseSeriesCastPage(id)
		self.ParseSeriesPhotoPageList(id)

		return self.meta

	def ParseSeriesCastPage(self,id):
		resp = urllib.urlopen( self.cast_url % id );
		soup = BeautifulSoup(resp.read(),fromEncoding="utf-8")

		pt = soup.find("h5",text=re.compile(u"^\s*출연\s*$"))
		if pt:
			for item in pt.parent.parent.findAll("dl"):
				name = item.find('img')['alt'].strip()
				role = item.find('span',{"class" : "etcs"}).string.strip()
				if role.rfind(u" 역") >= 0:
					role = role[:role.rfind(u" 역")]
				else:
					role = ''
				self.meta.s_actors.append( (name,role) )

		pt = soup.find("h5",text=re.compile(u"^\s*제작진\s*$"))
		if pt:
			for item in pt.parent.parent.findAll('li'):
				if item.contents[0].string.startswith(u"극본"):
					for person in item.contents[1:]:
						name = person.string.strip()
						if name:
							self.meta.s_writers.append(name)
				elif item.contents[0].string.startswith(u"연출"):
					for person in item.contents[1:]:
						name = person.string.strip()
						if name:
							self.meta.s_directors.append(name)

	def ParseSeriesPhotoPageList(self,id):
		this_url = self.photo_url % id
		self.ParseSeriesPhotoPage(this_url)

		resp = urllib.urlopen( this_url )
		strain = SoupStrainer("div",{"id" : "photoViewer"})
		soup = BeautifulSoup(resp.read(),fromEncoding="utf-8")
		for page in soup.find("div",{"class" : "pagination"}).findAll('a'):
			url = page['href']
			if not url.startswith("http"):
				if url[0] == '/':
					url = self.base_url+url
				else:
					url = self.base_url+'/'+url
			self.ParseSeriesPhotoPage(url)

	def ParseSeriesPhotoPage(self,url):
		resp = urllib.urlopen( url )
		strain = SoupStrainer("div",{"id" : "photoViewer"})
		soup = BeautifulSoup(resp.read(),strain,fromEncoding="utf-8")
		for item in soup.find("table",{"id" : "tPicTop"}).findAll("td"):
			img = item.find('img')['src']
			self.meta.s_backdrop_list.append( (img, re.sub('S\d{3}x\d{3}', 'image', img)) )

	#------------------------------------------
	def ParseEpisodePageList(self,id):
		self.EpisodeFound = False
		self.EpisodeInfo = {}
		self.last_epnum = 0
		self.ParseEpisodePageListByUrl( self.episode_url % id )
		for i in range(self.last_epnum-1):
			epnum = self.last_epnum-1-i
			self.meta.EpisodeInfo[(self.Season,epnum)] = ("제%d회"%epnum, "", "", "")

	def ParseEpisodePageListByUrl(self,url):
		#print url
		resp = urllib.urlopen(url);
		if not resp: return			# uncommon

		soup = BeautifulSoup(resp.read(),fromEncoding="utf-8")
		if soup.find("p", {"class" : "sorry"}):
			return			# not supported
		self.EpisodeFound = True
		self.GetEpisodeInfoByContent(soup,url)

		curpg = soup.find('span', {"class" : "current"})
		for pg in curpg.findNextSiblings('a'):
			url = self.episode_base_url+pg['href']
			if '~' in pg.contents[0]:
				self.ParseEpisodePageListByUrl(url)
			else:
				resp = urllib.urlopen(url)
				self.GetEpisodeInfoByContent( BeautifulSoup(resp.read(),fromEncoding="utf-8"), url )

	def GetEpisodeInfoByContent(self,soup,url):
		for item in soup.findAll('li',{'id' : re.compile("^itemId_")}):
			epnum = int( item['id'][item['id'].rfind('_')+1:] )
			if int(epnum) == 0:
				epnum = self.last_epnum-1
				url = ""
			if epnum <= 0: break
			titles = item.find("span",{"class" : "episode_num"}).string.split('&nbsp;')
			if url:
				ep_title = titles[0]
				ep_date = " ".join(titles[1:])
			else:
				ep_title = u"제%d회" % epnum
				ep_date = " ".join(titles)
			plot_blk = item.find("p",{"class" : "txt"})
			tit_stm = plot_blk.find("strong",{"class" : "epTit"})
			if tit_stm:
				ep_title = tit_stm.string
				ep_plot = tit_stm.nextSibling.nextSibling.nextSibling
				plot = unicode( self.striptags.sub('',str(ep_plot)).strip(), 'utf-8' )
			else:
				plot = unicode( self.striptags.sub('',plot_blk.renderContents()).strip(), 'utf-8' )
			self.meta.EpisodeInfo[(self.Season,epnum)] = (ep_title, ep_date, plot, url)
			#print "%d:%s:%s" % (epnum,titles[0]," ".join(titles[1:]))
			self.last_epnum = epnum

if __name__ == '__main__':
	fetcher = SeriesFetcher()

	print "search series"
	series = fetcher.Search(u"지붕 뚫고 하이킥")
	for id,title in series:
		print "%s: %s" % (id,title)

	id = series[0][0]
	print "parse series"
	meta = fetcher.ParseSeriesPage(id)
	print meta.__str__()

	fetcher.ParseEpisodePageList(52646)
	print fetcher.meta.GetEpisodeListXML("%d-%d")
	print fetcher.meta.GetEpisodeDetailXML(1,1)

	import os
	testdir = os.path.join('d:'+os.sep,'Videos','드라마','지붕 뚫고 하이킥')
	outfile = unicode(os.path.join(testdir,'tvshow.nfo'), 'utf-8')
	print "save nfo: %s" % outfile
	meta.SaveSeriesNFO( outfile )

	print "parse episode"
	fetcher.ParseEpisodePageList(id)
	print "found episode: %d" % len(meta.EpisodeInfo)
	if len(meta.EpisodeInfo) > 0:
		print "save episode metadata"
		outfile = unicode( os.path.join(testdir,'하이킥.EP 001.nfo'), 'utf-8' )
		meta.SaveEpisodeNFO(fetcher.Season, 1, outfile)
		outfile = unicode( os.path.join(testdir,'하이킥.EP 100.nfo'), 'utf-8' )
		meta.SaveEpisodeNFO(fetcher.Season, 100, outfile)
# vim: ts=4 sw=4