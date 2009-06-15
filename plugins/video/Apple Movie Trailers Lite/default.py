"""
    Plugin for streaming Apple Movie Trailers
"""

# main imports
import sys
import os
import xbmc

# plugin constants
__plugin__ = "Apple Movie Trailers Lite"
__author__ = "nuka1195"
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/plugins/video/Apple%20Movie%20Trailers%20Lite"
__credits__ = "Team XBMC"
__version__ = "1.7.3a"

xbmc.log( "[PLUGIN] '%s: version %s' initialized!" % ( __plugin__, __version__, ), xbmc.LOGNOTICE )


if ( __name__ == "__main__" ):
    if ( not sys.argv[ 2 ] ):
        import resources.lib.xbmcplugin_trailers as plugin
        plugin.Main()
    elif ( sys.argv[ 2 ].startswith( "?Fetch_Showtimes" ) ):
        import resources.lib.xbmcplugin_showtimes as showtimes
        s = showtimes.GUI( "plugin-AMTII-showtimes.xml", os.getcwd(), "default" )
        del s
    elif ( sys.argv[ 2 ].startswith( "?Download_Trailer" ) ):
        import resources.lib.xbmcplugin_download as download
        download.Main()
    elif ( sys.argv[ 2 ].startswith( "?OpenSettings" ) ):
        import xbmcplugin
        xbmcplugin.openSettings( sys.argv[ 0 ] )
        # sleep for a few milliseconds, to give dialog time to close.  had issues early, may not be necessary
        #TODO: verify this is necessary
        xbmc.sleep( 50 )
        # refresh listing in case settings changed
        xbmc.executebuiltin( "Container.Refresh" )

