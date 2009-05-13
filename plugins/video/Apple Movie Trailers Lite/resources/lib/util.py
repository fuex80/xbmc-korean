import os
import xbmc
import re

def get_filesystem( download_path ):
    # get the flavor of XBMC
    filesystem = os.environ.get( "OS", "xbox" )
    # use win32 illegal characters for smb shares to be safe (eg run on linux, save to windows)
    if ( download_path.startswith( "smb://" ) ):
        filesystem = "win32"
    return filesystem

def get_legal_filepath( title, url, mode, download_path, use_title, use_trailer ):
    # TODO: figure out how to determine download_path's filesystem, statvfs() not available on windows
    # different os's have different illegal characters
    illegal_characters = { "xbox": '\\/,*=|<>?;:\"+', "win32": '\\/*|<>?:\"', "Linux": "/", "OS X": "/:" }
    # get the flavor of XBMC
    environment = os.environ.get( "OS", "xbox" )
    # get the filesystem the trailer will be saved to
    filesystem = get_filesystem( download_path )
    # create our temp save path
    tmp_path = xbmc.translatePath( "special://temp/%s" % ( os.path.basename( url ), ) )
    # if play_mode is temp download to cache folder
    if ( mode < 2 ):
        filepath = tmp_path
    else:
        # get a valid filepath
        if ( use_title ):
            # append trailer if user preference
            trailer = ( "", "-trailer", )[ use_trailer ]
            # add trailer extension to trailer title
            title = title + trailer + os.path.splitext( url )[ 1 ]
        else:
            # we use the urls trailer name
            title = os.path.basename( url )
        # clean the filename
        filename = re.sub( '[%s]' % ( illegal_characters[ filesystem ], ), "_", title )
        # we need to handle xbox special
        if ( filesystem == "xbox" ):
            # set the length to 37 if filepath isn't a smb share for the .conf file
            if( len( filename ) > 37 and not download_path.startswith( "smb://" ) ):
                name, ext = os.path.splitext( filename )
                filename = name[ : 37 - len( ext ) ].strip() + ext
            # replace any characters whose ord > 127 for xbox filesystem
            if ( filesystem == "xbox" ):
                for char in filename:
                    if ( ord( char ) > 127 ):
                        filename = filename.replace( char, "_" )
        # make our filepath
        filepath = os.path.join( xbmc.translatePath( download_path ), filename )#, "utf-8", "replace" )
    # return results
    return tmp_path, filepath
