###################################################
# World in Chinese
# (c) 2007 Janne Tuukkanen
###################################################

from Tkinter import *
from  bubble import *
from wicframe import *
import time, random

class WICConnectors(WICFrame):
    class CBubble(Bubble):
        def __init__(self, canvas, x, y, width, height,
                     thickness=20, orientation='south',
                     text='', image=None, fill="", outline="black"):
            
            Bubble.__init__(self,canvas, x, y, width, height, thickness, orientation, text, image, fill, outline)

            self.connected_to = None
            self.key = None
            
    def __init__(self, bg_image=None, map_filename=None, master=None, lang1=None, lang2=None, numofwords=10, bg_color="#ffe7b6"):
        WICFrame.__init__(self, bg_image, map_filename)
        
        self.bg_color=bg_color
        self.numofwords = numofwords

        self.lang1, self.lang2 = lang1, lang2
        
        self.canvas.itemconfigure(self.bg_image, image="")
        self.canvas.configure(bg=bg_color)

        self.right_wrong_marks = []
        
        self.bubbles = { "left" : [], "right" : [] }
        self.words_in_bubbles = { "left" : [], "right" : [] }
        self.connections = {}
        self.words = []
        self.active_bubble = None
        
        self.createBubbles(self.numofwords)
        self.bindEventsToBubbles()
        
        self.setWords(numofwords, lang1, lang2)

        self.showReloadButton()

    def createBubbles(self, numofwords):
        x_left = 90
        x_right = 640
        x_right_wrong = 5
        y = 60
        w = 150
        h = 40
        pad = 10
        
        for i in range(numofwords):
            self.bubbles["left"].append(self.CBubble(self.canvas,
                                                     x_left, y, w, h,
                                                     orientation="east",
                                                     fill=self.bg_color))
            self.bubbles["right"].append(self.CBubble(self.canvas,
                                                      x_right, y, w, h,
                                                      orientation="west",
                                                      fill=self.bg_color))
            self.right_wrong_marks.append(self.canvas.create_image(x_right_wrong, y, anchor=N+W, tags="rightwrong"))
            y = y + h + pad

    def setWords(self, numofwords, lang1, lang2):                
        self.words = random.sample(self.dict.keys(), numofwords)

        self.words_in_bubbles["left"] = []
        self.words_in_bubbles["right"] = []
        
        for word in self.words:
            self.words_in_bubbles["left"].append([self.getWord(word, lang1), word])
            self.words_in_bubbles["right"].append([self.getWord(word, lang2), word])

        random.shuffle(self.words_in_bubbles["left"])
        random.shuffle(self.words_in_bubbles["right"])

        i = 0
        for l, r in zip(self.words_in_bubbles["left"],
                        self.words_in_bubbles["right"]):
            self.bubbles["left"][i].setWord(l[0])
            self.bubbles["left"][i].key = l[1]
            self.bubbles["right"][i].setWord(r[0])
            self.bubbles["right"][i].key = r[1]
            i = i + 1
            
    def bindEventsToBubbles(self):
        for l, r in zip(self.bubbles["left"], self.bubbles["right"]):
            l.bindEvent("<Button-1>", self.onClickEvent)
            r.bindEvent("<Button-1>", self.onClickEvent)
                    
    def onClickEvent(self, event, bubble):
        if bubble.connected_to != None:
            self.disconnectBubbles(bubble)
            return
        
        if self.active_bubble == None:
            self.active_bubble = bubble
            bubble.followMouse()
            return
        
        if self.active_bubble == bubble:
            self.active_bubble = None
            bubble.stopFollowingMouse()
            return
            
        if self.connectBubbles(bubble, self.active_bubble) == True:
            bubble.stopFollowingMouse()
            self.active_bubble = None

    def connectBubbles(self, bubble1, bubble2):
        c1 = bubble1.getCoords()
        c2 = bubble2.getCoords()

        # are bubbles already connected
        if  bubble1.connected_to != None or bubble2.connected_to != None:
            return False

        # both bubbles are on the same side on the screen
        if (c1[4] < 400 and c2[4] < 400) or (c1[4] > 400 and c2[4] > 400):
            return False

        coords = c1[4:] + c2[4:]

        bubble1.polyConfig(outline="")
        bubble1.tagRaise(bubble2.getPolygonId())
        bubble2.setCoords(coords)

        bubble1.connected_to = bubble2
        bubble2.connected_to = bubble1

        if self.allConnected():
            self.checkAnswers()
            
        return True
            
    def disconnectBubbles(self, bubble):
        if bubble == None:
            return
        
        if bubble.connected_to != None:
            bubble.connected_to.stopPointing()
            bubble.connected_to.connected_to = None
            bubble.connected_to.polyConfig(outline="black", fill=self.bg_color)
        
        bubble.stopPointing()
        bubble.connected_to = None
        bubble.polyConfig(outline="black", fill=self.bg_color)

    def disconnectAllBubbles(self):
        for bubble in self.bubbles["left"]:
            self.disconnectBubbles(bubble)

    def clearResults(self):
        self.canvas.itemconfigure("rightwrong", image="")
            
    def allConnected(self):
        for x in self.bubbles["left"]:
            if x.connected_to == None:
                return False
        return True
    
    def checkAnswers(self):
        r = w = i = 0
        for x in self.bubbles["left"]:
            l = x.key
            r = x.connected_to.key

            if l == r:
                self.canvas.itemconfigure(self.right_wrong_marks[i],
                                          image=self.right_icon)
            else:
                self.canvas.itemconfigure(self.right_wrong_marks[i],
                                          image=self.wrong_icon)
            i = i + 1

    def reloadClickEvent(self, event):
        self.disconnectAllBubbles()
        self.clearResults()
        self.setWords(self.numofwords, self.lang1, self.lang2)
        
if __name__ == "__main__":
    app = WICConnectors(lang1="Pinyin",
                        lang2="Simplified Chinese")
    app.mainloop()

