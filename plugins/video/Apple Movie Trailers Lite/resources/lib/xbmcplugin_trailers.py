"""
    Plugin for streaming Apple Movie Trailers
"""

# main imports
import sys
import os
import xbmc
import xbmcgui
import xbmcplugin

import time
import re
import urllib
import datetime
from xml.sax.saxutils import unescape

from util import get_filesystem, get_legal_filepath
from MediaWindow import MediaWindow, DirectoryItem


class _Parser:
    """
        Parses an xml document for videos
    """

    def __init__( self, xmlSource, settings, MediaWindow ):
        self.success = True
        self.settings = settings
        self.MediaWindow = MediaWindow
        # get our regions format
        self.date_format = xbmc.getRegion( "datelong" ).replace( "DDDD,", "" ).replace( "MMMM", "%B" ).replace( "D", "%d" ).replace( "YYYY", "%Y" ).strip()
        # get the list
        self.success = self._get_current_videos( xmlSource )

    def _get_current_videos( self, xmlSource ):
        try:
            mpaa_ratings = [ "G", "PG", "PG-13", "R", "NC-17" ]
            # encoding
            encoding = re.findall( "<\?xml version=\"[^\"]*\" encoding=\"([^\"]*)\"\?>", xmlSource )[ 0 ]
            # gather all video records <movieinfo>
            movies = re.findall( "<movieinfo[^>]*>(.*?)</movieinfo>", xmlSource )
            # enumerate thru the movie list and gather info
            for movie in movies:
                info = re.findall( "<info>(.*?)</info>", movie )
                cast = re.findall( "<cast>(.*?)</cast>", movie )
                genre = re.findall( "<genre>(.*?)</genre>", movie )
                poster = re.findall( "<poster>(.*?)</poster>", movie )
                preview = re.findall( "<preview>(.*?)</preview>", movie )
                # info
                title = unicode( unescape( re.findall( "<title>(.*?)</title>", info[ 0 ] )[ 0 ] ), encoding, "replace" )
                runtime = re.findall( "<runtime>(.*?)</runtime>", info[ 0 ] )[ 0 ]
                mpaa = re.findall( "<rating>(.*?)</rating>", info[ 0 ] )[ 0 ]
                rating_index = 0
                if ( self.settings[ "rating" ] < len( mpaa_ratings ) and mpaa in mpaa_ratings ):
                    rating_index = mpaa_ratings.index( mpaa )
                if ( rating_index > self.settings[ "rating" ] ):
                    continue
                studio = unicode( unescape( re.findall( "<studio>(.*?)</studio>", info[ 0 ] )[ 0 ] ), encoding, "replace" )
                postdate = ""
                tmp_postdate = re.findall( "<postdate>(.*?)</postdate>", info[ 0 ] )[ 0 ]
                if ( tmp_postdate ):
                    postdate = "%s-%s-%s" % ( tmp_postdate[ 8 : ], tmp_postdate[ 5 : 7 ], tmp_postdate[ : 4 ], )
                releasedate = re.findall( "<releasedate>(.*?)</releasedate>", info[ 0 ] )[ 0 ]
                if ( not releasedate ):
                    releasedate = ""
                copyright = unicode( unescape( re.findall( "<copyright>(.*?)</copyright>", info[ 0 ] )[ 0 ] ), encoding, "replace" )
                director = unicode( unescape( re.findall( "<director>(.*?)</director>", info[ 0 ] )[ 0 ] ), encoding, "replace" )
                plot = unicode( unescape( re.findall( "<description>(.*?)</description>", info[ 0 ] )[ 0 ] ), encoding, "replace" )
                # actors
                actors = []
                if ( cast ):
                    actor_list = re.findall( "<name>(.*?)</name>", cast[ 0 ] )
                    for actor in actor_list:
                        actors += [ unicode( unescape( actor ), encoding, "replace" ) ]
                # genres
                genres = []
                if ( genre ):
                    genres = re.findall( "<name>(.*?)</name>", genre[ 0 ] )
                genre = " / ".join( genres )
                # poster
                xlarge = re.findall( "<xlarge>(.*?)</xlarge>", poster[ 0 ] )
                location = re.findall( "<location>(.*?)</location>", poster[ 0 ] )
                if ( xlarge and self.settings[ "poster" ] ):
                    poster = xlarge[ 0 ]
                else:
                    poster = location[ 0 ]
                # trailer
                trailer = re.findall( "<large[^>]*>(.*?)</large>", preview[ 0 ] )[ 0 ]
                # replace with 1080p if quality == 1080p
                if ( self.settings[ "quality" ] == "_1080p" ):
                    trailer = trailer.replace( "a720p.m4v", "h1080p.mov" )
                # size
                size = long( re.findall( "filesize=\"([0-9]*)", preview[ 0 ] )[ 0 ] )
                # add the item to our media list
                ok = self._add_video( { "title": title, "runtime": runtime, "mpaa": mpaa, "studio": studio, "postdate": postdate, "releasedate": releasedate, "copyright": copyright, "director": director, "plot": plot, "cast": actors, "genre": genre, "poster": poster, "trailer": trailer, "size": size }, 0 )
                # if user cancels, call raise to exit loop
                if ( not ok ): raise
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            ok = False
        return ok

    def _add_video( self, video, total ):
        # get our media item
        dirItem = DirectoryItem()
        # set total items
        dirItem.totalItems = total
        try:
            # set the default icon
            icon = "DefaultVideo.png"
            # set an overlay if one is practical
            overlay = ( xbmcgui.ICON_OVERLAY_NONE, xbmcgui.ICON_OVERLAY_HD, )[ "720p." in video[ "trailer" ] or "1080p." in video[ "trailer" ] ]
            # only need to add label and thumbnail, setInfo() and addSortMethod() takes care of label2
            dirItem.listitem = xbmcgui.ListItem( video[ "title" ], iconImage=icon, thumbnailImage=video[ "poster" ] )
            # release date and year
            try:
                # format the date
                release_date = datetime.date( int( video[ "releasedate" ].split( "-" )[ 0 ] ), int( video[ "releasedate" ].split( "-" )[ 1 ] ), int( video[ "releasedate" ].split( "-" )[ 2 ] ) ).strftime( self.date_format )
                # we need just year also
                year = int( video[ "releasedate" ].split( "-" )[ 0 ] )
            except:
                release_date = ""
                year = 0
            # set the key information
            dirItem.listitem.setInfo( "video", { "Title": video[ "title" ], "Overlay": overlay, "Size": video[ "size" ], "Year": year, "Plot": video[ "plot" ], "PlotOutline": video[ "plot" ], "MPAA": video[ "mpaa" ], "Genre": video[ "genre" ], "Studio": video[ "studio" ], "Director": video[ "director" ], "Duration": video[ "runtime" ], "Cast": video[ "cast" ], "Date": video[ "postdate" ] } )
            # set release date property
            dirItem.listitem.setProperty( "releasedate", release_date )
            # get filepath and tmp_filepath
            tmp_path, filepath = get_legal_filepath( video[ "title" ], video[ "trailer" ], 2, self.settings[ "download_path" ], self.settings[ "use_title" ], self.settings[ "use_trailer" ] )
            # set context menu items
            items = [ ( xbmc.getLocalizedString( 30900 ), "XBMC.RunPlugin(%s?Fetch_Showtimes=True&title=%s)" % ( sys.argv[ 0 ], urllib.quote_plus( repr( video[ "title" ] ) ), ), ) ]
            # check if trailer already exists if user specified
            if ( self.settings[ "play_existing" ] and os.path.isfile( filepath.encode( "utf-8" ) ) ):
                dirItem.url = filepath
                # just add play trailer if trailer exists and user preference to always play existing
                items += [ ( xbmc.getLocalizedString( 30920 ), "XBMC.PlayMedia(%s)" % ( dirItem.url ), ) ]
            elif ( self.settings[ "play_mode" ] == 0 ):
                dirItem.url = video[ "trailer" ]
                # we want both play and download if user preference is to stream
                items += [ ( xbmc.getLocalizedString( 30910 ), "XBMC.RunPlugin(%s?Download_Trailer=True&trailer_url=%s)" % ( sys.argv[ 0 ], urllib.quote_plus( repr( video[ "trailer" ] ) ), ), ) ]
                items += [ ( xbmc.getLocalizedString( 30920 ), "XBMC.PlayMedia(%s)" % ( dirItem.url ), ) ]
            else:
                dirItem.url = "%s?Download_Trailer=True&trailer_url=%s" % ( sys.argv[ 0 ], urllib.quote_plus( repr( video[ "trailer" ] ) ) )
                # only add download if user prefernce is not stream
                items += [ ( xbmc.getLocalizedString( 30910 ), "XBMC.RunPlugin(%s?Download_Trailer=True&trailer_url=%s)" % ( sys.argv[ 0 ], urllib.quote_plus( repr( video[ "trailer" ] ) ), ), ) ]
            # add the movie information item
            items += [ ( xbmc.getLocalizedString( 30930 ), "XBMC.Action(Info)", ) ]
            # add settings menu item
            items += [ ( xbmc.getLocalizedString( 1045 ), "XBMC.RunPlugin(%s?OpenSettings)" % ( sys.argv[ 0 ], ) ) ]
            # add items to listitem with replaceItems = True so only ours show
            dirItem.listitem.addContextMenuItems( items, replaceItems=True )
            # add the item to the media list
            return self.MediaWindow.add( dirItem )
        except:
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            return False


class Main:
    # base url
    BASE_CURRENT_URL = "http://www.apple.com/trailers/home/xml/current%s.xml"

    # base paths
    BASE_DATA_PATH = os.path.join( xbmc.translatePath( "special://profile/" ), "plugin_data", "video", os.path.basename( os.getcwd() ) )
    BASE_CURRENT_SOURCE_PATH = os.path.join( xbmc.translatePath( "special://profile/" ), "plugin_data", "video", os.path.basename( os.getcwd() ), "current%s.xml" )

    def __init__( self ):
        # get users preference
        self._get_settings()
        # sort methods
        sortmethods = ( xbmcplugin.SORT_METHOD_LABEL, xbmcplugin.SORT_METHOD_SIZE, xbmcplugin.SORT_METHOD_DATE,
                                 xbmcplugin.SORT_METHOD_VIDEO_RUNTIME, xbmcplugin.SORT_METHOD_VIDEO_YEAR, xbmcplugin.SORT_METHOD_GENRE,
                                 xbmcplugin.SORT_METHOD_MPAA_RATING, xbmcplugin.SORT_METHOD_STUDIO, )
        # helper functions
        self.MediaWindow = MediaWindow( int( sys.argv[ 1 ] ), category=self.PluginCategory, content="movies", sortmethods=sortmethods, fanart=( self.settings[ "fanart_image" ], self.Fanart, ) )
        # set plugin buttons
        self._set_buttons()
        # fetch videos
        self.MediaWindow.end( self.get_videos() )

    def _set_buttons( self ):
        self.MediaWindow.setButton( 1045, onclick="XBMC.RunPlugin(%s?OpenSettings)" % ( sys.argv[ 0 ], ), bId=2 )

    def _get_settings( self ):
        self.settings = {}
        self.PluginCategory = ( xbmc.getLocalizedString( 30700 ), xbmc.getLocalizedString( 30701 ), xbmc.getLocalizedString( 30702 ), xbmc.getLocalizedString( 30703 ), )[ int( xbmcplugin.getSetting( "quality" ) ) ]
        self.Fanart = ( "standard", "480p", "720p", "1080p", )[ int( xbmcplugin.getSetting( "quality" ) ) ]
        self.settings[ "quality" ] = ( "", "_480p", "_720p", "_1080p", )[ int( xbmcplugin.getSetting( "quality" ) ) ]
        self.settings[ "poster" ] = ( xbmcplugin.getSetting( "poster" ) == "true" )
        self.settings[ "rating" ] = int( xbmcplugin.getSetting( "rating" ) )
        self.settings[ "download_path" ] = xbmcplugin.getSetting( "download_path" )
        self.settings[ "play_mode" ] = int( xbmcplugin.getSetting( "play_mode" ) )
        if ( self.settings[ "play_mode" ] == 2 and self.settings[ "download_path" ] == "" ):
            self.settings[ "play_mode" ] = 1
        self.settings[ "use_title" ] = ( xbmcplugin.getSetting( "use_title" ) == "true" and self.settings[ "download_path" ] != "" )
        self.settings[ "use_trailer" ] = ( xbmcplugin.getSetting( "use_trailer" ) == "true" and self.settings[ "use_title" ] == True and self.settings[ "download_path" ] != "" )
        self.settings[ "play_existing" ] = ( xbmcplugin.getSetting( "play_existing" ) == "true" and self.settings[ "download_path" ] != "" )
        self.settings[ "fanart_image" ] = xbmcplugin.getSetting( "fanart_image" )

    def get_videos( self ):
        ok = False
        # fetch xml source
        xmlSource = self.get_xml_source()
        # parse source and add our items
        if ( xmlSource ):
            ok = self.parse_xml_source( xmlSource )
        return ok

    def get_xml_source( self ):
        try:
            ok = True
            # set proper source
            base_path = self.BASE_CURRENT_SOURCE_PATH % ( self.settings[ "quality" ].replace( "_1080p", "_720p" ), )
            base_url = self.BASE_CURRENT_URL % ( self.settings[ "quality" ].replace( "_1080p", "_720p" ), )
            # get the source files date if it exists
            try: date = os.path.getmtime( base_path )
            except: date = 0
            # we only refresh if it's been more than a day, 24hr * 60min * 60sec
            refresh = ( ( time.time() - ( 24 * 60 * 60 ) ) >= date )
            # only fetch source if it's been more than a day
            if ( refresh ):
                # open url
                usock = urllib.urlopen( base_url )
            else:
                # open path
                usock = open( base_path, "r" )
            # read source
            xmlSource = usock.read()
            # close socket
            usock.close()
            # save the xmlSource for future parsing
            if ( refresh ):
                ok = self.save_xml_source( xmlSource )
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            ok = False
        if ( ok ):
            return xmlSource
        else:
            return ""

    def save_xml_source( self, xmlSource ):
        try:
            # set proper source
            base_path = self.BASE_CURRENT_SOURCE_PATH % ( self.settings[ "quality" ].replace( "_1080p", "_720p" ), )
            # if the path to the source file does not exist create it
            if ( not os.path.isdir( self.BASE_DATA_PATH ) ):
                os.makedirs( self.BASE_DATA_PATH )
            # open source path for writing
            file_object = open( base_path, "w" )
            # write xmlSource
            file_object.write( xmlSource )
            # close file object
            file_object.close()
            # return successful
            return True
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            return False

    def parse_xml_source( self, xmlSource ):
        # Parse xmlSource for videos
        parser = _Parser( xmlSource, self.settings, self.MediaWindow )
        return parser.success
