###################################################
# World in Chinese
# (c) 2007 Janne Tuukkanen
###################################################
from Tkinter import *
from  bubble import *
from wicframe import *
import time, random

class WICSelectRegion(WICFrame):                
    def __init__(self, bg_image=None, map_filename=None, master=None):
        WICFrame.__init__(self, bg_image, map_filename)

        self.word_pool = []
        self.current_word = ""

        self.main_bubble = MultiWordBubble(self.canvas,
                                           100,520,600,60,
                                           self.langs.keys(),
                                           orientation="north",
                                           buttons=True)
        self.main_bubble.polyConfig(fill="#ffe7b6")
        self.main_bubble.followMouse()

        random.seed()
        
        self.setRegionEvents()

        self.setCurrentWord("beijing")

        self.showHelpButton()
        
        self.nextWord()
        
    def setRegionEvents(self):
        for key, x in self.regions.iteritems():

            def handler_in(event, self=self, key=key):
                return self.__enterRegionEvent(event, key)
            self.canvas.tag_bind(key, "<Enter>", handler_in)

            def handler_out(event, self=self, key=key):
                return self.__exitRegionEvent(event, key)
            self.canvas.tag_bind(key, "<Leave>", handler_out)
            
            def handler_click(event, self=self, key=key):
                return self.__clickRegionEvent(event, key)
            self.canvas.tag_bind(key, "<Button-1>", handler_click)


    def helpClickEvent(self, event):
        self.hiLiOn(self.current_word)
    
    def __clickRegionEvent(self, event, region):
        
        if region == self.current_word:
            self.showRight()
            self.nextWord()
        else:
            self.showWrong()
            
    def __enterRegionEvent(self, event, region):
        self.hiLiOn(region)

    def __exitRegionEvent(self, event, region):
        self.hiLiOff(region)

    def setCurrentWord(self, key):
        self.current_word = key
        for lang in self.langs.keys():
            self.main_bubble.setWord(lang, self.getWord(key, lang))


    def nextWord(self):
        if self.word_pool == []:
            self.word_pool = self.dict.keys()
            random.shuffle(self.word_pool)
            
        self.setCurrentWord(self.word_pool.pop())
        
        
if __name__ == "__main__":
    app = WICSelectRegion()
    app.mainloop()

