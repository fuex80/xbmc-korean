"""
Showtimes module

Nuka1195
"""

import sys
import xbmcgui

import showtimesScraper
ShowtimesFetcher = showtimesScraper.ShowtimesFetcher()
from utilities import *

_ = sys.modules[ "__main__" ].__language__
__scriptname__ = sys.modules[ "__main__" ].__scriptname__
__version__ = sys.modules[ "__main__" ].__version__
__svn_url__ = sys.modules[ "__main__" ].__svn_url__
__svn_revision__ = sys.modules[ "__main__" ].__svn_revision__


class GUI( xbmcgui.WindowXMLDialog ):
    def __init__( self, *args, **kwargs ):
        xbmcgui.WindowXMLDialog.__init__( self, *args, **kwargs )
        self.title = kwargs[ "title" ]
        self.location = kwargs[ "location" ]
        self.doModal()

    def onInit( self ):
        xbmcgui.lock()
        self._show_dialog()
        xbmcgui.unlock()
        self._get_showtimes()

    def _show_dialog( self ):
        self.getControl( 20 ).setLabel( self.title )
        self.getControl( 30 ).setLabel( "%s: %s" % ( _( 603 ), self.location ), )
        self.getControl( 40 ).setLabel( "%s:" % _( 602 ) )
        self.getControl( 50 ).setLabel( "" )
        self.getControl( 100 ).reset()
        self.getControl( 100 ).addItem( _( 601 ) )

    def _get_showtimes( self ):
        date, self.movie_showtimes = ShowtimesFetcher.get_showtimes( self.title, self.location )
        if ( date is None ): date = _( 600 )
        else: date = "%s: %s" % ( _( 602 ), date, )
        self.getControl( 40 ).setLabel( date )
        self._fill_list()

    def _get_selection( self, choice ):
        self.getControl( 20 ).setLabel( choice )
        self.getControl( 30 ).setLabel( self.movie_showtimes[ choice ][ 0 ] )
        self.getControl( 40 ).setLabel( "%s:" % _( 602 ) )
        self.getControl( 50 ).setLabel( self.movie_showtimes[ choice ][ 2 ] )
        self.getControl( 100 ).reset()
        self.getControl( 100 ).addItem( _( 601 ) )
        date, self.movie_showtimes = ShowtimesFetcher.get_selection( self.movie_showtimes[ choice ][ 3 ] )
        self.getControl( 40 ).setLabel( "%s: %s" % ( _( 602 ), date, ) )
        self._fill_list()

    def _fill_list( self ):
        self.getControl( 100 ).reset()
        if ( self.movie_showtimes ):
            self.theaters = self.movie_showtimes.keys()
            self.theaters.sort()
            for theater in self.theaters:
                list_item = xbmcgui.ListItem( theater, self.movie_showtimes[ theater ][ 1 ], self.movie_showtimes[ theater ][ 0 ], self.movie_showtimes[ theater ][ 2 ] )
                self.getControl( 100 ).addItem( list_item )
        else:
            self.getControl( 100 ).addItem( _( 600 ) )

    def _close_dialog( self ):
        self.close()

    def onClick( self, controlId ):
        self._get_selection( self.theaters[ self.getControl( controlId ).getSelectedPosition() ] )

    def onFocus( self, controlId ):
        pass

    def onAction( self, action ):
        if ( action in ACTION_CANCEL_DIALOG ):
            self._close_dialog()
