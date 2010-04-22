# -*- coding: utf-8 -*-
import urllib2,md5
import string,re

def qple_jamak_from_file(f):
    qple_home = 'http://www.tokplayer.com'

    f.seek(100*1024)
    buff1 = f.read(100*1024)    # 100KB starting at 100KB
    f.seek(0)
    buff2 = f.read(50*1024)     # 50KB starting at 0
    f.seek(100*1024)
    buff2 += f.read(50*1024)    # 50KB starting at 100KB

    # calculate MD5 key from file
    m = md5.new(); m.update(buff1); key1 = m.hexdigest()
    m = md5.new(); m.update(buff2); key2 = m.hexdigest()

    queryAddr1 = qple_home+"/app/subtitle/view_subtitle.html?q_hash=%s&q_newhash=%s"%(key1,key2)
    print "search subtitle at %s"%queryAddr1
    req = urllib2.Request(queryAddr1)
    resp = urllib2.urlopen(req)
    link = resp.read(); resp.close()

    match = re.search('''location.replace\('([^']*)'\)''',link)
    if match is None or "/notice/" in match.group(1):
	return []

    # parse result page
    queryAddr2 = qple_home+match.group(1)
    print "parse search result at %s"%queryAddr2
    req = urllib2.Request(queryAddr2)
    req.add_header('Referer', queryAddr1)
    resp = urllib2.urlopen(req)
    link = resp.read(); resp.close()

    # regular search result page
    url_match  = re.compile(u'''<a href="([^"]*)"[^>]*>\[다운로드 링크\]</a>'''.encode("euc-kr")).findall(link)
    tit_match = re.compile('''<td class="txt_[^>]*>([^<]*)</td>''').findall(link)
    if len(url_match) == 0 or len(url_match) != len(tit_match): 
	print "Unusual result page, "+queryAddr2
	return []

    ###----- Select a subtitle to download
    title_list = []
    for i in range(0,len(url_match)):
	title_list.append( ('qple', string.strip(tit_match[i]), qple_home+url_match[i]) )
    return title_list