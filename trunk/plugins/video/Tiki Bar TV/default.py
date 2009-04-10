import urllib,urllib2,re,xbmcplugin,xbmcgui

#TikiBar TV for XBMC by exiledx

def CATEGORIES():
        addDir('Season 1','http://www.tikibartv.com/?page_id=221',2,'')
        addDir('Season 2','http://www.tikibartv.com/?page_id=223',1,'')
        addDir('Season 3','http://www.tikibartv.com/?page_id=225',1,'')
        addDir('Season 4','http://www.tikibartv.com/?page_id=227',1,'')
        addDir('Season 5','http://www.tikibartv.com/?page_id=33',1,'')

def INDEX(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('<img src="(.+?)" width=".+?" height=".+?" /></a></p>\n<p><a href="(.+?)">(.+?)</a>').findall(link)
	for img,url,name in match:
		addDir(name,'http://www.tikibartv.com/'+url,3,'http://www.tikibartv.com/'+img)

def INDEX2(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('<img src="(.+?)" width=".+?" height=".+?" /></a></p>\n<p><a href="(.+?)">(.+?)</a>').findall(link)
	for img,url,name in match:
		addDir(name,'http://www.tikibartv.com/'+url,4,'http://www.tikibartv.com/'+img)



def VIDEOLINKS(url,name):
        LinkFill = True
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        try:
                msn=re.compile('<title>Tiki Bar TV   &raquo; Episode (.+?):.+?</title>').findall(link)
                for url in msn:
                        addLink('Play '+name,'http://media.libsyn.com/media/tiki/TikiBarTV_'+url+'.mov','')
        except: pass

def VIDEOLINKS2(url,name):
        LinkFill = True
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        if url == 'http://www.tikibartv.com/?page_id=177':
                addLink('Play '+name,'http://media.libsyn.com/media/tiki/TikiBarTV_01.mov','')
        if url == 'http://www.tikibartv.com/?page_id=175':
                addLink('Play '+name,'http://media.libsyn.com/media/tiki/TikiBarTV_02.mov','')
        if url == 'http://www.tikibartv.com/?page_id=172':
                addLink('Play '+name,'http://media.libsyn.com/media/tiki/TikiBarTV_03.mov','')
        if url == 'http://www.tikibartv.com/?page_id=170':
                addLink('Play '+name,'http://media.libsyn.com/media/tiki/TikiBarTV_04.mov','')
        if url == 'http://www.tikibartv.com/?page_id=168':
                addLink('Play '+name,'http://media.libsyn.com/media/tiki/TikiBarTV_05.mov','')
        if url == 'http://www.tikibartv.com/?page_id=166':
                addLink('Play '+name,'http://media.libsyn.com/media/tiki/TikiBarTV_06.mov','')
        if url == 'http://www.tikibartv.com/?page_id=164':
                addLink('Play '+name,'http://media.libsyn.com/media/tiki/TikiBarTV_07.mov','')
        if url == 'http://www.tikibartv.com/?page_id=162':
                addLink('Play '+name,'http://media.libsyn.com/media/tiki/TikiBarTV_08.mov','')
        if url == 'http://www.tikibartv.com/?page_id=160':
                addLink('Play '+name,'http://media.libsyn.com/media/tiki/TikiBarTV_09.mov','')
        if url == 'http://www.tikibartv.com/?page_id=158':
                addLink('Play '+name,'http://media.libsyn.com/media/tiki/TikiBarTV_A10.mov','')
        if url == 'http://www.tikibartv.com/?page_id=156':
                addLink('Play '+name,'http://media.libsyn.com/media/tiki/TikiBarTV_10.mov','')
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
        INDEX2(url)

elif mode==3:
        print ""+url
        VIDEOLINKS(url,name)

elif mode==4:
        print ""+url
        VIDEOLINKS2(url,name)




xbmcplugin.endOfDirectory(int(sys.argv[1]))
