import urllib,urllib2,re,xbmcplugin,xbmcgui

#DramaCrazy for XBMC by exiledx

def CATEGORIES():
        addDir('Short Films','http://www.wongfuproductions.com/ShortsIndex.html',2,'http://www.wongfuproductions.com/video/Shortsheader.jpg')
        addDir('Music Videos','http://www.wongfuproductions.com/MVsIndex.html',2,'http://www.wongfuproductions.com/MVs/MVheader.jpg')
        addDir('The Tour Documentary','http://www.wongfuproductions.com/TourIndex.html',2,'http://www.wongfuproductions.com/video/Tourheader.jpg')
        addDir('Video Blogs','http://www.wongfuproductions.com/BlogIndex.html',2,'http://www.wongfuproductions.com/Blog/Blogheader.jpg')

def INDEX(url):
        if url == 'http://www.wongfuproductions.com/ShortsIndex.html':
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<a href="Shorts(.+?)" target="_blank"><img src="(.+?)"').findall(link)
                xx=0
                for url,img in match:
                        xx=xx+1
                        name = 'Short Film #' + str(int(xx))
                        addDir(name,'http://www.wongfuproductions.com/'+url,4,'http://www.wongfuproductions.com/'+img)
        if url == 'http://www.wongfuproductions.com/MVsIndex.html':
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<a href="MVs(.+?)" target="_blank"><img src="(.+?)"').findall(link)
                xx=0
                for url,img in match:
                        xx=xx+1
                        name = 'Music Video #' + str(int(xx))
                        addDir(name,'http://www.wongfuproductions.com/'+url,4,'http://www.wongfuproductions.com/'+img)
        if url == 'http://www.wongfuproductions.com/TourIndex.html':
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<a href="(.+?)" target="_blank"><img src="(.+?)"').findall(link)
                xx=0
                for url,img in match:
                        xx=xx+1
                        name = 'Tour Episode #' + str(int(xx))
                        addDir(name,url,4,'http://www.wongfuproductions.com/'+img)
        if url == 'http://www.wongfuproductions.com/BlogIndex.html':
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<a href="(.+?)" target="_blank"><img src="(.+?)"').findall(link)
                xx=0
                for url,img in match:
                        xx=xx+1
                        name = 'Video Blog #' + str(int(xx))
                        addDir(name,url,4,'http://www.wongfuproductions.com/'+img)


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
                p=re.compile('<param name="movie" value="http://www.veoh.com/videodetails.+?permalinkId=(.+?)" />')
                match=p.findall(link)
                for code in match:
                        veoh='http://127.0.0.1:64653/'+match[0]+"?.avi"
                        addLink("Play "+name,veoh,"http://www.veoh.com/static/marketing/wallpapers/Veoh_Logo1680.jpg")
        except: pass
        #DAILYMOTION
        try:
                p=re.compile('<param name="movie" value="http://www.dailymotion.com/swf/(.+?)" />')
                match=p.findall(link)
                for a in match:
                        f=urllib2.urlopen("http://keepvid.com/?url=http://www.dailymotion.com/swf/"+str(a))
                        myspace=f.read()
                        comp=re.compile('to download<br /><br /><a href="(.+?)\r\n"')
                        for url in comp.findall(myspace):
                                addLink ('Play '+name,url,'')
        except: pass
        #GOOGLE
        try:
                p=re.compile('<param name="movie" value="http://video.google.com/googleplayer.swf.+?docId=(.+?)" />')
                match=p.findall(link)
                for a in match:
                        f=urllib2.urlopen("http://keepvid.com/?url=http://video.google.com/videoplay?docid="+str(a))
                        myspace=f.read()
                        comp=re.compile('to download<br /><br /><a href="(.+?)\r\n"')
                        for url in comp.findall(myspace):
                                addLink ('Play '+name,url,'http://www.movie2k.com/img/google.gif')
        except: pass
        #YOUTUBE
        try:
                p=re.compile('"video_id": "(.+?)",')
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
        try:
                p=re.compile('<embed src="http://www.youtube.com/v/(.+?)" type=".+?"')
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
        #MYSPACE
        try:
                p=re.compile('<param name="movie" value="http://mediaservices.myspace.com/services/media/embed.aspx/m=(.+?),t=1,mt=video,ap=0" />')
                match=p.findall(link)
                for a in match:
                        f=urllib2.urlopen("http://mediaservices.myspace.com/services/rss.ashx?type=video&mediaID="+str(a))
                        myspace=f.read()
                        comp=re.compile('<media:content url="(.+?)"')
                        for url in comp.findall(myspace):
                                addLink ('Play '+name,url,'')
        except: pass
        #YAHOO
        try:
                yimg=re.compile('<param name="movie" value="http://d.yimg.com/static.video.yahoo.com/yep/YV_YEP.swf.+?id=(.+?)&amp;intl=us" />').findall(link)
                for url in yimg:
                        req = urllib2.Request('http://cosmos.bcst.yahoo.com/up/yep/process/getPlaylistFOP.php?node_id='+url)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                        response = urllib2.urlopen(req).read()
                        SERVER=re.compile('<STREAM APP="(.+?)"').findall(response)
                        URL=re.compile('FULLPATH="(.+?)"').findall(response)
                        FINAL=(SERVER[0]+URL[0]).replace('&amp;','&')
                        addLink('Play '+name,FINAL,'')
        except:pass
        #MEGAVIDEO
        try:
                mv=re.compile('<param name="movie" value="http://wwwstatic.megavideo.com/mv_player.swf.+?v=(.+)" />').findall(link)
                mvlinks=mv[0][:8]
                req = urllib2.Request("http://www.megavideo.com/xml/videolink.php?v="+mvlinks)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                req.add_header('Referer', 'http://www.megavideo.com/')
                lemon = urllib2.urlopen(req);response=lemon.read();lemon.close()
                errort = re.compile(' errortext="(.+?)"').findall(response)
                if len(errort) > 0: addLink(errort[0],'http://novid.com','')
                else:
                        s = re.compile(' s="(.+?)"').findall(response)
                        k1 = re.compile(' k1="(.+?)"').findall(response)
                        k2 = re.compile(' k2="(.+?)"').findall(response)
                        un = re.compile(' un="(.+?)"').findall(response)
                        movielink = "http://www" + s[0] + ".megavideo.com/files/" + decrypt(un[0], k1[0], k2[0]) + "/"
                        addLink('Play '+name, movielink+'?.flv','')
        except: pass

####################################################################################################################
# MegaVideo Routine
####################################################################################################################
        
#Python Video Decryption and resolving routines.
#Courtesy of Voinage, Coolblaze.
#Megavideo - Coolblaze # Part 1 put this below VIDEOLINKS function.

def ajoin(arr):
    strtest = ''
    for num in range(len(arr)):
        strtest = strtest + str(arr[num])
    return strtest

def asplit(mystring):
    arr = []
    for num in range(len(mystring)):
        arr.append(mystring[num])
    return arr
        
def decrypt(str1, key1, key2):

    __reg1 = []
    __reg3 = 0
    while (__reg3 < len(str1)):
        __reg0 = str1[__reg3]
        holder = __reg0
        if (holder == "0"):
            __reg1.append("0000")
        else:
            if (__reg0 == "1"):
                __reg1.append("0001")
            else:
                if (__reg0 == "2"): 
                    __reg1.append("0010")
                else: 
                    if (__reg0 == "3"):
                        __reg1.append("0011")
                    else: 
                        if (__reg0 == "4"):
                            __reg1.append("0100")
                        else: 
                            if (__reg0 == "5"):
                                __reg1.append("0101")
                            else: 
                                if (__reg0 == "6"):
                                    __reg1.append("0110")
                                else: 
                                    if (__reg0 == "7"):
                                        __reg1.append("0111")
                                    else: 
                                        if (__reg0 == "8"):
                                            __reg1.append("1000")
                                        else: 
                                            if (__reg0 == "9"):
                                                __reg1.append("1001")
                                            else: 
                                                if (__reg0 == "a"):
                                                    __reg1.append("1010")
                                                else: 
                                                    if (__reg0 == "b"):
                                                        __reg1.append("1011")
                                                    else: 
                                                        if (__reg0 == "c"):
                                                            __reg1.append("1100")
                                                        else: 
                                                            if (__reg0 == "d"):
                                                                __reg1.append("1101")
                                                            else: 
                                                                if (__reg0 == "e"):
                                                                    __reg1.append("1110")
                                                                else: 
                                                                    if (__reg0 == "f"):
                                                                        __reg1.append("1111")

        __reg3 = __reg3 + 1

    mtstr = ajoin(__reg1)
    __reg1 = asplit(mtstr)
    __reg6 = []
    __reg3 = 0
    while (__reg3 < 384):
    
        key1 = (int(key1) * 11 + 77213) % 81371
        key2 = (int(key2) * 17 + 92717) % 192811
        __reg6.append((int(key1) + int(key2)) % 128)
        __reg3 = __reg3 + 1
    
    __reg3 = 256
    while (__reg3 >= 0):

        __reg5 = __reg6[__reg3]
        __reg4 = __reg3 % 128
        __reg8 = __reg1[__reg5]
        __reg1[__reg5] = __reg1[__reg4]
        __reg1[__reg4] = __reg8
        __reg3 = __reg3 - 1
    
    __reg3 = 0
    while (__reg3 < 128):
    
        __reg1[__reg3] = int(__reg1[__reg3]) ^ int(__reg6[__reg3 + 256]) & 1
        __reg3 = __reg3 + 1

    __reg12 = ajoin(__reg1)
    __reg7 = []
    __reg3 = 0
    while (__reg3 < len(__reg12)):

        __reg9 = __reg12[__reg3:__reg3 + 4]
        __reg7.append(__reg9)
        __reg3 = __reg3 + 4
        
    
    __reg2 = []
    __reg3 = 0
    while (__reg3 < len(__reg7)):
        __reg0 = __reg7[__reg3]
        holder2 = __reg0
    
        if (holder2 == "0000"):
            __reg2.append("0")
        else: 
            if (__reg0 == "0001"):
                __reg2.append("1")
            else: 
                if (__reg0 == "0010"):
                    __reg2.append("2")
                else: 
                    if (__reg0 == "0011"):
                        __reg2.append("3")
                    else: 
                        if (__reg0 == "0100"):
                            __reg2.append("4")
                        else: 
                            if (__reg0 == "0101"): 
                                __reg2.append("5")
                            else: 
                                if (__reg0 == "0110"): 
                                    __reg2.append("6")
                                else: 
                                    if (__reg0 == "0111"): 
                                        __reg2.append("7")
                                    else: 
                                        if (__reg0 == "1000"): 
                                            __reg2.append("8")
                                        else: 
                                            if (__reg0 == "1001"): 
                                                __reg2.append("9")
                                            else: 
                                                if (__reg0 == "1010"): 
                                                    __reg2.append("a")
                                                else: 
                                                    if (__reg0 == "1011"): 
                                                        __reg2.append("b")
                                                    else: 
                                                        if (__reg0 == "1100"): 
                                                            __reg2.append("c")
                                                        else: 
                                                            if (__reg0 == "1101"): 
                                                                __reg2.append("d")
                                                            else: 
                                                                if (__reg0 == "1110"): 
                                                                    __reg2.append("e")
                                                                else: 
                                                                    if (__reg0 == "1111"): 
                                                                        __reg2.append("f")
                                                                    
        __reg3 = __reg3 + 1

    endstr = ajoin(__reg2)
    return endstr
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
########END OF PART 1
#Part 2
# To activate it just call Megavideo(url) - where url is your megavideo url.
def Megavideo(url,info):
    if len(url)<=35:
        mega=re.sub('http://www.megavideo.com/v/','',url)
    else:
        mega=url[27:35]
    req = urllib2.Request("http://www.megavideo.com/xml/videolink.php?v="+mega)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    req.add_header('Referer', 'http://www.megavideo.com/')
    page = urllib2.urlopen(req);response=page.read();page.close()
    errort = re.compile(' errortext="(.+?)"').findall(response)
    if len(errort) > 0:
        addLink(errort[0], '',4, '', '')
    else:
        s = re.compile(' s="(.+?)"').findall(response)
        k1 = re.compile(' k1="(.+?)"').findall(response)
        k2 = re.compile(' k2="(.+?)"').findall(response)
        un = re.compile(' un="(.+?)"').findall(response)
        movielink = "http://www" + s[0] + ".megavideo.com/files/" + decrypt(un[0], k1[0], k2[0]) + "/"
        title = 'MEGAVIDEO '
        addLink(name, movielink+'?.flv',4,'http://www.movie2k.com/img/mega.gif',info)
##
#####END OF PART 2




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
        PAGES(url)

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
