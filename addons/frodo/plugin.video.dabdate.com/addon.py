# -*- coding: utf-8 -*-
"""
  Dabdate - Korea Drama/TV Shows Streaming Service
"""
from xbmcswift2 import Plugin, actions
import os
import resources.lib.dabdate as dabdate

plugin = Plugin()
_L = plugin.get_string

qualcode = {
    ''        :'1',     # default
    _L(31000) :'1',     # medium
    _L(31001) :'2',     # low
    _L(31002) :'3',     # high
}
localcode = {
    ''        :'la',    # default
    _L(31010) :'au',    # austrailia
    _L(31011) :'eu',    # europe
    _L(31012) :'sa',    # south america
    _L(31013) :'la',    # US west
    _L(31014) :'ny',    # US east
}

#CookiePath = xbmc.translatePath( 'special://temp/dabdate_cookie.lwp' )
CookiePath = os.path.join(plugin.storage_path, 'cookie.lwp')

tPrevPage = u"[B]<<%s[/B]" % _L(30200)
tNextPage = u"[B]%s>>[/B]" % _L(30201)

@plugin.route('/', name='browse_top', options={'url':'/'})
@plugin.route('/browse/<url>')
def browse_page(url):
    quality = qualcode[ plugin.get_setting("quality", unicode) ]
    localsrv = localcode[ plugin.get_setting("local", unicode) ]
    info = dabdate.parseTop( dabdate.root_url+url, quality=quality, localsrv=localsrv )
    items = []
    label_download = plugin.get_string(30204)
    for item in info['video']:
        if item['free']:
            title = u"[B]%s[/B]"% item['title']
        else:
            title = item['title']
        items.append({
            'label':title,
            'path':plugin.url_for('play_video', url=item['url']),
            'thumbnail':item['thumb'],
            'context_menu': [
                (label_download, actions.background(plugin.url_for('download_video', url=item['url'])))
            ]
        })
    # navigation
    if 'prevpage' in info:
        items.append({'label':tPrevPage, 'path':plugin.url_for('browse_page', url=info['prevpage'])})
    if 'nextpage' in info:
        items.append({'label':tNextPage, 'path':plugin.url_for('browse_page', url=info['nextpage'])})
    # extra 
    if url == '/':
        items.append({'label':u"[COLOR FF0000FF]유아프로그램[/COLOR]", 'path':plugin.url_for('browse_page', url="?lang=5")})
        #items.append({'label':u"[COLOR FF0000FF]그때를 아십니까[/COLOR]", 'path':plugin.url_for('browse_page', url="?lang=7")})
        #items.append({'label':u"[COLOR FF0000FF]특선 다큐멘터리[/COLOR]", 'path':plugin.url_for('browse_page', url="?lang=6")})
    morepage = True if 'page=' in url else False
    return plugin.finish(items, update_listing=morepage)

@plugin.route('/play/<url>')
def play_video(url):
    info = resolve_video_url(url)
    vid_url = "{0:s}|User-Agent={1:s}&Cookie={2:s}".format(info['url'], info['useragent'], info['cookie'])
    #return plugin.play_video({'label':info['title'], 'path':vid_url, 'is_playable':True})
    from xbmcswift2 import xbmcgui
    li = xbmcgui.ListItem(info['title'], iconImage="DefaultVideo.png")
    li.setInfo('video', {"Title": info['title']})
    xbmc.Player().play(vid_url, li)
    return plugin.finish(None, succeeded=False)

@plugin.route('/download/<url>')
def download_video(url):
    info = resolve_video_url(url)
    wdir = plugin.get_setting('download_dir', unicode)
    ext = '.mp4'
    import xbmcvfs
    if not xbmcvfs.exists(wdir):
        return plugin.finish(None, succeeded=False)
    wpath = wdir + info['title']+ext
    print 'Download path: '+wpath.encode('utf-8')
    import urllib2
    req = urllib2.Request(info['url'])
    req.add_header('User-Agent', info['useragent'])
    req.add_header('Cookie', info['cookie'])
    plugin.notify('Downloading to '+wpath.encode('utf-8'))
    r = urllib2.urlopen(req)
    f = xbmcvfs.File(wpath, 'w')
    while True:
        buf = r.read(512*1024)
        if len(buf) == 0:
            break
        f.write(buf)
    r.close()
    f.close()
    plugin.notify('Download completed and saved as '+wpath.encode('utf-8'))
    return plugin.finish(None, succeeded=True)

def resolve_video_url(url):
    from xbmcswift2 import xbmc
    userid = plugin.get_setting('id', str)
    passwd = plugin.get_setting('pass', str)

    page_url = dabdate.root_url+url
    return dabdate.getStreamUrl( page_url, userid=userid, passwd=passwd, cookiefile=CookiePath )

if __name__ == "__main__":
    plugin.run()

# vim:sw=4:sts=4:et
