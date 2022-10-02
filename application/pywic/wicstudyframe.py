###################################################
# World in Chinese
# (c) 2007 Janne Tuukkanen
###################################################
from Tkinter import *
from wicframe import *
from bubble import *
import random
import time

class WICStudyFrame(WICFrame):
    class Animation:
        def __init__(self, master, canvas, items, target_x, target_y, steps=50, item_key=None):

            self.__items = []
            self.target_x, self.target_y = target_x, target_y
            self.master = master
            self.canvas = canvas
            self.active = True
            self.item_key = item_key
            

            for item in items:
                x = random.uniform(0, 800)
                y = random.uniform(0, 600)
                dx = (target_x - x) / steps
                dy = (target_y - y) / steps

                if type(item) == str:
                    self.__items.append([self.canvas.create_text(x, y, text=item, font=("Times", 10)), dx, dy])
                else:
                    #self.canvas.create_image(100,100,image=item)
                    self.__items.append([self.canvas.create_image(x, y, image=item), dx, dy])

            if self.item_key != None:
                self.master.hiLiOn(self.item_key)

            self.run()
            
        def run(self):
            if not self.active:
                if self.item_key != None:
                    self.master.hiLiOff(self.item_key)
                return
            
            self.active = False
            
            for item in self.__items:
                dx = item[1]
                dy = item[2]
                if dx  == 0 and dy  == 0:
                    continue
                self.active = True
                c = self.canvas.coords(item[0])
                if self.__isNear(c[0], c[1], self.target_x, self.target_y):
                    item[1] = item[2] = 0
                    self.canvas.delete(item[0])

                self.canvas.move(item[0], dx, dy)

            self.master.after(20, self.run)

        def __isNear(self, x1, y1, x2, y2, distance=10):
            if abs(x1 - x2) < distance and abs(y1 - y2) < distance:
                return True
            return False
            
        def stop(self):
            for item in items:
                self.canvas.delete(item[0])
            
    def __init__(self, bg_image=None, map_filename=None, master=None):
        WICFrame.__init__(self, bg_image, map_filename)
        self.grid()
        
        self.main_bubble = Bubble(self.canvas, 10,10,700,60)

        self.__initTexts()

        self.__initAnimationButton()
        
        self.main_bubble.followMouse()

        self.__activateBubble()


    def __initTexts(self):
        self.word_image = [None, None, None, None]
        self.word_image[0] = self.canvas.create_image(150, 40)
        self.word_image[1] = self.canvas.create_image(290, 40)
        self.word_image[2] = self.canvas.create_image(430, 40)
        self.word_image[3] = self.canvas.create_image(570, 40)

        self.word_text = [None, None, None, None]
        self.word_text[0] = self.canvas.create_text(130, 40)
        self.word_text[1] = self.canvas.create_text(250, 40)
        self.word_text[2] = self.canvas.create_text(370, 40)
        self.word_text[3] = self.canvas.create_text(490, 40)

        self.setLanguages()

    def setLanguages(self, lang1=None, lang2=None, lang3=None, lang4=None):
        self.word_lang = [None, None, None, None]

        self.word_lang[0] = lang1
        self.word_lang[1] = lang2
        self.word_lang[2] = lang3
        self.word_lang[3] = lang4
        
    def __setRegionEvents(self):
        for key, x in self.regions.iteritems():
            def handler_in(event, self=self, key=key):
                return self.__enterRegionEvent(event, key)
            self.canvas.tag_bind(key, "<Enter>", handler_in)
            def handler_out(event, self=self, key=key):
                return self.__exitRegionEvent(event, key)
            self.canvas.tag_bind(key, "<Leave>", handler_out)

    def __clearRegionEvents(self):
        for key, x in self.regions.iteritems():
            self.canvas.tag_unbind(key, "<Enter>")
            

    def __enterRegionEvent(self, event, region_key):
        for i in range(4):
            word = self.getWord(region_key, self.word_lang[i])

            if word == None:
                continue
            if type(word) == str:
                self.canvas.itemconfigure(self.word_text[i], text=word)
                continue
            
            self.canvas.itemconfigure(self.word_image[i], image=word)

        self.hiLiOn(region_key)
                
    def __exitRegionEvent(self, event, region_key):
        for i in range(4):
            self.canvas.itemconfigure(self.word_text[i], text="")
            self.canvas.itemconfigure(self.word_image[i], image="")
            
        self.hiLiOff(region_key)

    def __initAnimationButton(self):
        self.__animation_start_image = PhotoImage(file="images/start.gif")
        self.__animation_stop_image = PhotoImage(file="images/stop.gif")

        self.__animation_button = self.canvas.create_image(400,540)

        self.canvas.tag_bind(self.__animation_button,"<Button-1>", self.toggleAnimation)
        
        self.__animationDeactivate()

    def __animationDeactivate(self):
        self.canvas.itemconfigure(self.__animation_button,
                                  image=self.__animation_start_image)
        self.__animation_active = False
        self.__activateBubble()

    def __animationActivate(self):
        self.canvas.itemconfigure(self.__animation_button,
                                  image=self.__animation_stop_image)
        self.__animation_active = True
        self.__deactivateBubble()
        self.__playAnimation()
        
    def toggleAnimation(self, event=None):
        if self.__animation_active:
            self.__animationDeactivate()
        else:
            self.__animationActivate()

    def __playAnimation(self):
        if not self.__animation_active:
            return
        
        key = random.choice(self.dict.keys())
        
        #key = "beijing"
        dicts = self.dict[key]
        items = []
        for lang, word in dicts[0].iteritems():
            items.append(word)
        for lang, image in dicts[1].iteritems():
            items.append(image)
        target_x = self.map_points[key][0]
        target_y = self.map_points[key][1]
        a = self.Animation(self, self.canvas, items, target_x, target_y, steps=100, item_key=key)

        self.after(2000, self.__playAnimation)
        
    def __deactivateBubble(self):
        for i in range(4):
            self.canvas.itemconfigure(self.word_image[i], image="")
            self.canvas.itemconfigure(self.word_text[i], text="")
            self.main_bubble.polyConfig(fill="#ffe7b6", outline="")
            self.main_bubble.stopFollowingMouse()

        self.__clearRegionEvents()

    
    def __activateBubble(self):
        self.main_bubble.polyConfig(fill="#ffe7b6", outline="black")
        self.__setRegionEvents()
        self.main_bubble.followMouse()

        self.__setRegionEvents()
    
          
if __name__ == '__main__':
    app = WICStudyFrame()
    #app.main_bubble.polyConfig(fill="#ffe7b6")
    app.setLanguages("English", "Simplified Chinese",
                     "Traditional Chinese", "Pinyin")
    #app.main_bubble.followMouse()
    app.mainloop()


        
