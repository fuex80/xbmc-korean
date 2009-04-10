import urllib,urllib2,re,xbmcplugin,xbmcgui

#MonkeySee for XBMC by exiledx

def CATEGORIES():
        addDir('Auto and Mechanical','http://www.monkeysee.com/main/category/1-auto-and-mechanical',1,'')
        addDir('Beauty and Fashion','http://www.monkeysee.com/main/category/2-beauty-and-fashion',1,'')
        addDir('Careers and Education','http://www.monkeysee.com/main/category/17-careers-and-education',1,'')
        addDir('Food and Drink','http://www.monkeysee.com/main/category/4-food-and-drink',1,'')
        addDir('Games and Gaming','http://www.monkeysee.com/main/category/19-games-and-gaming',1,'')
        addDir('Health and Fitness','http://www.monkeysee.com/main/category/5-health-and-fitness',1,'')
        addDir('Hobbies and Crafts','http://www.monkeysee.com/main/category/6-hobbies-and-crafts',1,'')
        addDir('Holidays and Seasonal','http://www.monkeysee.com/main/category/15-holidays-and-seasonal',1,'')
        addDir('Home and Garden','http://www.monkeysee.com/main/category/7-home-and-garden',1,'')    
        addDir('Love and Relationships','http://www.monkeysee.com/main/category/18-love-and-relationships',1,'')
        addDir('Music and Dance','http://www.monkeysee.com/main/category/9-music-and-dance',1,'')
        addDir('Other','http://www.monkeysee.com/main/category/13-other',1,'')
        addDir('Parenting','http://www.monkeysee.com/main/category/10-parenting',1,'')
        addDir('Personal Finance','http://www.monkeysee.com/main/category/186-personal-finance',1,'')
        addDir('Pets','http://www.monkeysee.com/main/category/11-pets',1,'')
        addDir('Safety','http://www.monkeysee.com/main/category/20-safety',1,'')
        addDir('Sports and Leisure','http://www.monkeysee.com/main/category/12-sports-and-leisure',1,'')

def SUBCATS(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
        match=re.compile('<a href="(.+?)" class="subcat_link">(.+?)</a></li>').findall(link)
        for url,name in match:
                if name.find('&amp;')>1:
                        rev=name.replace('amp;','')
                        addDir(rev,'http://www.monkeysee.com'+url,2,'')
                if name.find('&amp;')<1:
                        addDir(name,'http://www.monkeysee.com'+url,2,'')
        
def INDEX(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	pgsrc=urllib2.urlopen(req).read()
	link=response.read()
	response.close()
	match=re.compile('<div class="title"><h3><a href="(.+?)">(.+?)</a>').findall(link)
	for url,name in match:
                if name.find ('&quot;')>1:
                        rev=name.replace('&quot;', '')
                        addDir(rev,'http://www.monkeysee.com'+url,3,'')
                if name.find ('&quot;')<1:
                        addDir(name,'http://www.monkeysee.com'+url,3,'')
	if pgsrc.find('">Next &gt;&gt;</a>')>1:
                match=re.compile('<a href="(.+?)">Next').findall(link)
                for url in match:
                        addDir(' Next Page','http://www.monkeysee.com'+url,2,'')
	

def PARTS(url):
        req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	try:
                match=re.compile('src="(.+?).gif.+?" width="154" /></a></div>\n  <div class="title"><h3><a href="(.+?)">(.+?)</a>').findall(link)
                for img,url,name in match:
                        if name.find ('&quot;')>1:
                                rev=name.replace('&quot;', '')
                                addDir(rev,'http://www.monkeysee.com'+url,4,'http://www.monkeysee.com'+img+'.gif')
                        if name.find ('&quot;')<1:
                                addDir(name,'http://www.monkeysee.com'+url,4,'http://www.monkeysee.com'+img+'.gif')
                patch=re.compile('src="(.+?).gif.+?" width="154" /></a></div>\n  <div class="title_playing"><h3><a href="(.+?)">(.+?)</a>').findall(link)
                for img,url,name in patch:
                        if name.find ('&quot;')>1:
                                rev=name.replace('&quot;', '')
                                addDir(rev,'http://www.monkeysee.com'+url,4,'http://www.monkeysee.com'+img+'.gif')
                        if name.find ('&quot;')<1:
                                addDir(name,'http://www.monkeysee.com'+url,4,'http://www.monkeysee.com'+img+'.gif')
        except: pass
	try:
                match=re.compile('src="(.+?).jpg.+?" width="154" /></a></div>\n  <div class="title"><h3><a href="(.+?)">(.+?)</a>').findall(link)
                for img,url,name in match:
                        if name.find ('&quot;')>1:
                                rev=name.replace('&quot;', '')
                                addDir(rev,'http://www.monkeysee.com'+url,4,'http://www.monkeysee.com'+img+'.jpg')
                        if name.find ('&quot;')<1:
                                addDir(name,'http://www.monkeysee.com'+url,4,'http://www.monkeysee.com'+img+'.jpg')
                patch=re.compile('src="(.+?).jpg.+?" width="154" /></a></div>\n  <div class="title_playing"><h3><a href="(.+?)">(.+?)</a>').findall(link)
                for img,url,name in patch:
                        if name.find ('&quot;')>1:
                                rev=name.replace('&quot;', '')
                                addDir(rev,'http://www.monkeysee.com'+url,4,'http://www.monkeysee.com'+img+'.jpg')
                        if name.find ('&quot;')<1:
                                addDir(name,'http://www.monkeysee.com'+url,4,'http://www.monkeysee.com'+img+'.jpg')
        except: pass
        try:
                match=re.compile('src="(.+?)" width="154" /></a></div>\n  <div class="title"><h3><a href="(.+?)">(.+?)</a>').findall(link)
                for img,url,name in match:
                        if name.find ('&quot;')>1:
                                rev=name.replace('&quot;', '')
                                addDir(rev,'http://www.monkeysee.com'+url,4,img)
                        if name.find ('&quot;')<1:
                                addDir(name,'http://www.monkeysee.com'+url,4,img)
                patch=re.compile('src="(.+?)" width="154" /></a></div>\n  <div class="title_playing"><h3><a href="(.+?)">(.+?)</a>').findall(link)
                for img,url,name in patch:
                        if name.find ('&quot;')>1:
                                rev=name.replace('&quot;', '')
                                addDir(rev,'http://www.monkeysee.com'+url,4,img)
                        if name.find ('&quot;')<1:
                                addDir(name,'http://www.monkeysee.com'+url,4,img)
        except: pass



def VIDEOLINKS(url,name):
        LinkFill = True
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        videoid=re.compile('"videoId", "(.+?)"').findall(link)
        clipid=re.compile('"clipId", "(.+?)"').findall(link)
        combined=videoid+clipid
        f=urllib2.urlopen('http://www.monkeysee.com/play/'+combined[0]+'/response_'+combined[1]+'.xml')
        myspace=f.read()
        comp=re.compile('<File>(.+?)</File>')
        for url in comp.findall(myspace):
                addLink ('Play '+name,url,'')


def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        SUBCATS(url)

elif mode==2:
        print ""+url
        INDEX(url)

elif mode==3:
        print ""+url
        PARTS(url)

elif mode==4:
        print ""+url
        VIDEOLINKS(url,name)





xbmcplugin.endOfDirectory(int(sys.argv[1]))
