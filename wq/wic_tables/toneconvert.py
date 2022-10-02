#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import sys


class ToneConvert:
    
    def __init__(self):
        self.TONE = ["", "&#x304;", "&#x301;", "&#x30C;", "&#x300;", "" ]
        
    def getTones(self, s):
        # strip leading and trailing whitespaces
        s = s.lstrip()
        s = s.rstrip()

        if s == "":
            return None
        
        word = ""
        line = ""
        tones = []
        x = 0
        r = []
        
        for c in s:
            if c.isdigit():
                tone = int(c)
                if tone > -1 and tone < 6 and word != "":
                    r.append([word, tone])
                    word = ""
                    continue
            if c.isspace():
                r.append([word, 0])
                word = ""
            else:
                word = word + c

        return r
    
    def lastVowel(self, word):
        vowels = [u"a", u"e", u"i", u"o", u"u", u"ü", u"A", u"E",
                  u"I", u"O", u"U", u"Ü"]
        s = word.lower()

        i = -1
        for v in vowels:
            j = s.rfind(v)
            if j > i:
                i = j

        return i
        
    def tonePlace(self, word):
        s = word.lower()
        
        i = word.find("a")
        if i != -1:
            return i
        i = word.find("e")
        if i != -1:
            return i
        i = word.find("ou")
        if i != -1:
            return i
        return self.lastVowel(s)

    def getToned(self, word, tone):
        i = self.tonePlace(word)
        if i == -1:
            return word
        return word[:i+1] + self.TONE[tone] + word[i+1:]
    
    def processFile(self, infile, outfile):
        """ dictionary is in format asciitext0;pinyintext0\n
            asciitext1;pinyintext1\n ... asciitextN;pinyintextN\n
            gif image of pinyintexttN is saved as asciitextN.gif"""

        # this is UTF-8, so we us 'codecs'
        FILE = codecs.open(infile, "r", "utf-8")
        lines = FILE.readlines()
        FILE.close()

        FILE = codecs.open(outfile, "w", "utf-8")

        FILE.write("<html><head><title>pinyin</title>")
        FILE.write('<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">')
        FILE.write("</head><body>\n")
        FILE.write("<table border='1'>\n")
        
        for line in lines:
            s = ""

            line = line.strip()
            if line.isspace():
                continue
            a = line.split(";")

            s = "<tr><td>%s</td><td>" % a[0]

            words = self.getTones(a[1])
            for w in words:
                s = s + self.getToned(w[0], w[1])
                
            s = s + "</td>"
            s = s + "<td>%s</td><td>%s</td><td>%s</td>" % (a[2], a[3], a[4])
            s = s + "</tr>\n"
            FILE.write(s)
            #filename = self.out_path + "/" + a[0] + ".gif"
            #self.converter.imageToFile(a[1], filename)

        FILE.write("</table></body></html>\n")
        FILE.close()
            
if __name__ == '__main__':
    argslen = len(sys.argv)
    
    if  argslen != 3:
        sys.stderr.write("Usage: toneconvert.py <infile> <outfile>")
        sys.exit()

        
    c = ToneConvert()
    
    c.processFile(sys.argv[1], sys.argv[2])


