import urllib,urllib2,re,xbmcplugin,xbmcgui

#JohnLocker for XBMC by exiledx

def CATEGORIES():
        addDir('New Releases','http://johnlocker.com/all-videos/new-releases/',1,'')
        addDir('Conspiracy','http://johnlocker.com/all-videos/conspiracy/',1,'')
        addDir('History','http://johnlocker.com/all-videos/history/',1,'')
        addDir('US History','http://johnlocker.com/all-videos/us-history.html',1,'')
        addDir('World History','http://johnlocker.com/all-videos/world-history.html',1,'')
        addDir('Political','http://johnlocker.com/all-videos/political/',1,'')
        addDir('Religious','http://johnlocker.com/all-videos/religious/',1,'')
        addDir('Science','http://johnlocker.com/all-videos/science/',1,'')
        addDir('Sports','http://johnlocker.com/all-videos/sports/',1,'')
        addDir('Weird','http://johnlocker.com/all-videos/weird/',1,'')
        addDir('Music','http://johnlocker.com/all-videos/music/',1,'')


def INDEX(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	pgsrc=urllib2.urlopen(req).read()
	link=response.read()
	response.close()
	match=re.compile('<div class="videotitleintabbedlist"><a href="{videolink}"><div><a href="(.+?)">(.+?)</a></div></a></div>').findall(link)
	for url,name in match:
		addDir(name,url,2,'')
	if pgsrc.find('http://johnlocker.com/components/com_seyret/themes/default/images/right.png')>1:
                match=re.compile('<a href="(.+?)"><img src="http://johnlocker.com/components/com_seyret/themes/default/images/right.png" border="0">').findall(link)
                for url in match:
                        addDir(' Next Page',url,1,'')

def VIDEOLINKS(url,name):
        LinkFill = True
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        #VEOH
        try:
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                p=re.compile("<div id=.+? style=.+?><div id=.+?><embed src='http://www.veoh.com/videodetails.swf.+?permalinkId=(.+?)&id=1&player=videodetails&videoAutoPlay=0")
                match=p.findall(link)
                for code in match:
                        veoh='http://127.0.0.1:64653/'+match[0]+"?.avi"
                        addLink("Play "+name,veoh,"http://www.veoh.com/static/marketing/wallpapers/Veoh_Logo1680.jpg")
        except: pass
        #GUBA
        try:
                guba=re.compile("file=http://free.guba.com/uploaditem/(.+?)/flash.flv&image=.+?&showdigits=false&autostart=false&logo=.+?' /></embed></div><div id=.+?>").findall(link)
                for url in guba:
                        addLink('Play '+name,'http://free.guba.com/uploaditem/'+url+'/flash.flv','')
        except: pass
        #GOOGLE
        try:
                p=re.compile('<div id="originalvideolink"><a href="http://video.google.com/videoplay.+?docid=(.+?)" target="_blank">')
                match=p.findall(link)
                for a in match:
                        f=urllib2.urlopen("http://www.flashvideodownloader.org/download.php?u=http://video.google.com/videoplay?docid="+str(a))
                        myspace=f.read()
                        comp=re.compile('<a href="(.+?)" title="Click to Download"><font color=red>')
                        for url in comp.findall(myspace):
                                addLink ('Play '+name,url,'')
        except: pass
        try:
                p=re.compile('<div id="originalvideolink"><a href="http://video.google.com/videoplay.+?docid=(.+?)&.+?" target="_blank">')
                match=p.findall(link)
                for a in match:
                        f=urllib2.urlopen("http://www.flashvideodownloader.org/download.php?u=http://video.google.com/videoplay?docid="+str(a))
                        myspace=f.read()
                        comp=re.compile('<a href="(.+?)" title="Click to Download"><font color=red>')
                        for url in comp.findall(myspace):
                                addLink ('Play '+name,url,'')
        except: pass
        #YOUTUBE
        try:
                p=re.compile('<div id="originalvideolink"><a href="http://www.youtube.com/watch.+?v=(.+?)" target="_blank">')
                match=p.findall(link)
                for code in match:
                        print 'code='+code
                        req = urllib2.Request('http://www.youtube.com/watch?v='+code)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                        response = urllib2.urlopen(req)
                        link=response.read()
                        response.close()
                        p=re.compile('"t": "(.+?)"')
                        match=p.findall(link)
                        for blah in match:
                                linkage="http://www.youtube.com/get_video?video_id="+code+"&t="+blah+"&fmt=18"
                                addLink ('Play '+name,linkage,'')
        except: pass
        #GOOGLEALT
        try:
                p=re.compile('<div id="originalvideolink"><a href="http://video.google.com/videofeed.+?docid=(.+?)" target="_blank">')
                match=p.findall(link)
                for a in match:
                        f=urllib2.urlopen("http://www.flashvideodownloader.org/download.php?u=http://video.google.com/videoplay?docid="+str(a))
                        myspace=f.read()
                        comp=re.compile('<a href="(.+?)" title="Click to Download"><font color=red>')
                        for url in comp.findall(myspace):
                                addLink ('Play '+name,url,'')
        except: pass
                
      

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
        INDEX(url)

elif mode==2:
        print ""+url
        VIDEOLINKS(url,name)





xbmcplugin.endOfDirectory(int(sys.argv[1]))
