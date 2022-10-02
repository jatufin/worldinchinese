###################################################
# World in Chinese
# (c) 2007 Janne Tuukkanen
###################################################
from Tkinter import *
from  bubble import *
from wicframe import *
import time, random

class WICSelectWord(WICFrame):
    class FourBubbles:
        class FBubble(Bubble):
            def __init__(self, canvas, x, y, width, height,
                         thickness=20, orientation='south',
                         text='', image=None, fill="", outline="black"):
                
                Bubble.__init__(self,canvas, x, y, width, height,
                                thickness, orientation, text, image,
                                fill, outline)
                self.key = None
                self.x0, self.y0 = x, y
                self.x1, self.y1 = x + width, y + height
                

            def isInside(self, x, y):
                if x < self.x0 or x > self.x1:
                    return False
                if y < self.y0 or y > self.y1:
                    return False
                return True

        def __init__(self, canvas, x, y, width, height, color="white"):
            self.bubbles = []
            #self.current_word = None
            self.current = None
            
            w = width/4 - 5
            for i in range(4):
                b = self.FBubble(canvas,
                                 x + i * (w + 5), y,
                                 w, height)
                self.bubbles.append(b)
                b.bindEvent("<Enter>", self.mouseEnterEvent)
                b.polyConfig(fill=color)
                
        def setWords(self, words):
            for b, w in zip(self.bubbles, words):
                b.setWord(w)
        
        def setKeys(self, keys):
            for b, k in zip(self.bubbles, keys):
                b.key=k

        def mouseEnterEvent(self, event, bubble):
            for b in self.bubbles:
                b.polyConfig(outline="black")
            bubble.polyConfig(outline="#AAAAAA")
            self.current = bubble.key

        def isInside(self, x, y):
            for b in self.bubbles:
                if b.isInside(x,y):
                    return True
            return False
        
    def __init__(self, bg_image=None, map_filename=None, master=None):
        WICFrame.__init__(self, bg_image, map_filename)

        self.word_pool = []
        self.current_word = None
        self.current_keys = None
        self.current_lang = "English"

        self.bubbles = self.FourBubbles(self.canvas, 10, 530, 780, 60, "#ffe7b6")

        self.canvas.bind("<Button-1>", self.clickEvent)

        self.langSelectButtons()
        random.seed()

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

    def clickEvent(self, event):
        if not self.bubbles.isInside(event.x, event.y):
            return
        
        if self.bubbles.current == self.current_word:
            self.showRight()
            self.hiLiOff(self.current_word)
            self.nextWord()
        else:
            self.showWrong()

    def langSelectButtons(self):
        x = 150
        dx = 150
        y = 10
        for lang in self.langs:
            t=self.canvas.create_text(x, y, text=lang, font=("Helvetica", 10))
            def langButton(event, lang=lang):
                self.setLang(lang)
            self.canvas.tag_bind(t, "<Button-1>", langButton)
            x += dx
        
    def helpClickEvent(self, event):
        pass
    
    def __clickRegionEvent(self, event, region):
        pass
            
    def __enterRegionEvent(self, event, region):
        pass

    def __exitRegionEvent(self, event, region):
        pass


    def nextWord(self):
        if self.word_pool == []:
            self.word_pool = self.dict.keys()
            random.shuffle(self.word_pool)
            
        self.current_word = self.word_pool.pop()
        self.hiLiOn(self.current_word)
        while(True):
            keys = random.sample(self.dict.keys(), 3)
            if keys.count(self.current_word) == 0:
                break
        keys.append(self.current_word)
        random.shuffle(keys)
        self.setWords(keys)

    def setWords(self, keys):
        self.current_keys = keys
        words = []
        for k in keys:
            w = self.getWord(k, self.current_lang)
            words.append(w)

        self.bubbles.setWords(words)
        self.bubbles.setKeys(keys)

    def setLang(self, lang):
        self.current_lang=lang
        self.setWords(self.current_keys)
        
if __name__ == "__main__":
    app = WICSelectRegion()
    app.mainloop()

