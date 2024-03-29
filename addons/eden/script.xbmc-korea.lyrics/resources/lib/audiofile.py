﻿# -*- Mode: python; coding: utf-8; tab-width: 8; indent-tabs-mode: t; -*-
"""
read audio stream from audio file
"""

import os
import struct

class AudioFile(object):
    f = None
    audioStart = 0

    def AudioFile(self):
        self.f = None
        self.audioStart = 0

    def Open(self,file):
        self.audioStart = 0
	self.f = open(file,'rb')
	ext = os.path.splitext(file)[1].lower()
	if   ext == '.mp3':  self.AnalyzeMp3()
	elif ext == '.ogg':  self.AnalyzeOgg()
	elif ext == '.wma':  self.AnalyzeWma()
	#elif ext == '.flac':  self.AnalyzeFlac()
	elif ext == '.flac': pass
	elif ext == '.ape': pass
	elif ext == '.wav': pass
	else:	# not supported format
	    self.f.close()
	    self.f = None
	    raise UnknownFormat

    def Close(self):
        self.f.close()
	self.f = None

    def ReadAudioStream(self, len, offset=0):
	self.f.seek(self.audioStart+offset, 0)
	return self.f.read(len)

    def AnalyzeMp3(self):
        # Searching ID3v2 tag
        while True:
            buf = self.f.read(3)
            if len(buf) < 3 or self.f.tell() > 50000:
                # ID tag is not found
                self.f.seek(0,0)
                self.audioStart = 0
                return
            if buf == 'ID3':
                self.f.seek(3,1)     # skip version/flag
                # ID length (synchsafe integer)
                tl = struct.unpack('4b', self.f.read(4))
                taglen = (tl[0]<<21)|(tl[1]<<14)|(tl[2]<<7)|tl[3]
                self.f.seek(taglen,1)
                break
            self.f.seek(-2,1)
        # Searching MPEG SOF
        while True:
            buf = self.f.read(1)
            if len(buf) < 1 or self.f.tell() > 1000000:
                raise FormatError
            if buf == '\xff':
                rbit = struct.unpack('B',self.f.read(1))[0] >> 5
                if rbit == 7:   # 11 1's in total
                    self.f.seek(-2,1)
                    self.audioStart = self.f.tell()
                    return

    def AnalyzeOgg(self):
        # Parse page (OggS)
        while True:
            buf = self.f.read(27)    # header 
            if len(buf) < 27 or self.f.tell() > 50000:
                # parse error
                raise FormatError
            if buf[0:4] != 'OggS':
                # not supported page format
                raise UnknownFormat
            numseg = struct.unpack('B', buf[26])[0]
            #print "#seg: %d" % numseg

            segtbl = struct.unpack('%dB'%numseg, self.f.read(numseg))    # segment table
            for seglen in segtbl:
                buf = self.f.read(7)    # segment header 
            	#print "segLen(%s): %d" % (buf[1:7],seglen)
                if buf == "\x05vorbis":
                    self.f.seek(-7,1)   # rollback
                    self.audioStart = self.f.tell()
		    return
            	self.f.seek(seglen-7,1)	# skip to next segment

    def AnalyzeWma(self):
        # Searching GUID
        while True:
            buf = self.f.read(16)
            if len(buf) < 16 or self.f.tell() > 50000:
                raise FormatError
            guid = buf.encode("hex");
            if guid == "3626b2758e66cf11a6d900aa0062ce6c":
            	# ASF_Data_Object
                self.f.seek(-16,1)     # rollback
		self.audioStart = self.f.tell()
                return
            else:
                objlen = struct.unpack('<Q', self.f.read(8))[0]
                self.f.seek(objlen-24,1)     # jump to next object

    def AnalyzeFlac(self):
        if self.f.read(4) != 'fLaC':
	    raise UnknownFormat
        # Searching GUID
        while True:
            buf = self.f.read(4)
            if len(buf) < 16 or self.f.tell() > 50000:
                # not found
                raise FormatError
            metalen = buf[1] | (buf[2]<<8) | (buf[3]<<16);
            self.f.seek(metalen,1)   # skip this metadata block
            if buf[0] & 0x80:
            	# it was the last metadata block
		self.audioStart = self.f.tell()
                return

if ( __name__ == '__main__' ):
    analyzer = AudioFile()
    testdir = os.path.join('d:'+os.sep,'Music','test')+os.sep

    analyzer.Open(testdir+'test.mp3')
    print "mp3: "+analyzer.ReadAudioStream(10).encode("hex")
    analyzer.Close()

    analyzer.Open(testdir+'test.ogg')
    print "ogg: "+analyzer.ReadAudioStream(10).encode("hex")
    analyzer.Close()

    analyzer.Open(testdir+'test.wma')
    print "wma: "+analyzer.ReadAudioStream(10).encode("hex")
    analyzer.Close()

    analyzer.Open(testdir+'test.flac')
    print "flac: "+analyzer.ReadAudioStream(10).encode("hex")
    analyzer.Close()

    analyzer.Open(testdir+'test.wav')
    print "wav: "+analyzer.ReadAudioStream(10).encode("hex")
    analyzer.Close()
