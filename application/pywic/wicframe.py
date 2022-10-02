# -*- coding: utf_8 -*-
###################################################
# World in Chinese
# (c) 2007 Janne Tuukkanen
###################################################
from Tkinter import *



class WICFrame(Frame):
    def createStuff(self, bg_image, map_filename):
        #self.grid()

        # class variables
        if bg_image == None:
            self.bg_image_filename = "images/background.gif"
        else:
            self.bg_image_filename = bg_image
        if map_filename == None:
            self.map_filename = "regions.csv"
        else:
            self.map_filename = map_filename
            
        self.dict = {}
        self.langs = {}
        self.map_points = {}
        self.regions = {}
        self.highlight_images = {}
        
        self.__createCanvas()
        self.__loadHighlights()
        self.__standardButtons()
        self.__loadMapFile()

        self.__setRegionEvents()

        self.__loadDictionaries("keys.csv", textdicts="textdicts.csv",
                                imagedicts="imagedicts.csv")


    def __createCanvas(self):
        self.canvas = Canvas(self, width=800, height=600, background="white",
                             highlightthickness=0)

        self.canvas.grid()
        
        # background image
        if self.bg_image_filename != None:
            self.img = PhotoImage(file=self.bg_image_filename)
            self.bg_image = self.canvas.create_image(400,300, image=self.img)
            self.canvas.itemconfigure(self.bg_image, tag="background")

    def __exitEvent(self, event):
        self.quit()
        
    def __standardButtons(self):
        self.__exit_image = PhotoImage(file="images/exit.gif")
        exit_id = self.canvas.create_image(800, 0, image=self.__exit_image,
                                           anchor = N+E)
        self.canvas.tag_bind(exit_id, "<Double-Button-1>", self.__exitEvent)

        self.help_icon = PhotoImage(file="images/help.gif")
        self.help_image = self.canvas.create_image(30,30)

        self.reload_icon = PhotoImage(file="images/reload.gif")
        self.reload_image = self.canvas.create_image(400,580)

        self.right_icon = PhotoImage(file="images/right.gif")
        self.wrong_icon = PhotoImage(file="images/wrong.gif")
        self.right_wrong = self.canvas.create_image(400,40)

    def showHelpButton(self):
        self.canvas.itemconfigure(self.help_image,
                                  image = self.help_icon)
        self.canvas.tag_bind(self.help_image,
                             "<Button-1>", self.helpClickEvent)


    def showReloadButton(self):
        self.canvas.itemconfigure(self.reload_image,
                                  image = self.reload_icon)
        self.canvas.tag_bind(self.reload_image,
                             "<Button-1>",
                             self.reloadClickEvent)
    
    def hideHelpButton(self):
        self.canvas.itemconfigure(self.help_image,
                                  image = "")
    
    def hideReloadButton(self):
        self.canvas.itemconfigure(self.reload_image,
                                  image = "")

    def helpClickEvent(self, event):
        pass

    def reloadClickEvent(self, event):
        pass

    def showRight(self):
        self.canvas.itemconfigure(self.right_wrong,
                                  image = self.right_icon)

    def showWrong(self):
        self.canvas.itemconfigure(self.right_wrong,
                                  image = self.wrong_icon)
    def hideRightWrong(self):
        self.canvas.itemconfigure(self.right_wrong, image="")
        
    def __loadMapFile(self):
        FILE = open(self.map_filename, "r")
        objects = FILE.readlines()

        
        for line in objects[1:]: #first line contains headers, it's omitted
            o = line.split(";")
            object_tags = o[0]
            object_type = o[1]
            object_fill = o[2]
            object_outline = o[3]
                
            if o[4] == "bezier":
                object_smooth = 1
            else:
                object_smooth = 0
                
            # coord strings are converted to floats                
            object_coords = [float(x) for x in o[5][1:-2].split(",")]
            
            # point objects are not added in canvas, but in
            # dictionary, with object_tags as key
            if object_type == "point":
                self.map_points[object_tags] = object_coords
                continue

            # canvas objects
            cob = -1
            if object_type == "polygon":
                cob = self.canvas.create_polygon(object_coords,
                                                 smooth=object_smooth,
                                                 fill="", #object_fill,
                                                 outline="", #object_outline,
                                                 tags = object_tags)

            # these map objects are tagged as regions
            if cob != -1:
                self.regions[object_tags] = None
                self.canvas.addtag_withtag("region", cob)
                
        FILE.close()

        #self.testPoints()
            
    # TEST TEST TEST
    def testPoints(self):
        for key, point in self.map_points.iteritems():
            self.canvas.create_line(0,0,point[0],point[1], arrow=LAST, fill="red")
            
    def __loadDictionaries(self, keyfile, textdicts="", imagedicts=""):
##     keyfile contains keys on the dictionary
##     texdicts is a file listing filenames of dictionaries in csv format
##     imagedicts is a file containing paths to image files
##     gif images named key.gif
##
##     self.dict is in format {"key" = [{"lang" = "word", ... },
##                                      {"lang" = image, ...  }]}

        keys = self.__loadKeys(keyfile)

        textd = self.__loadDicts(textdicts)

        for lang, filename in textd:
            self.langs[lang] = "active"
            d = self.__loadTextDictFile(filename)
            for key, word in d.iteritems():
                self.dict[key][0][lang] = word

        imaged = self.__loadDicts(imagedicts)
        
        for lang, path in imaged:
            self.langs[lang] = "active"
            for key in keys:
                filename = path + key + ".gif"
                
                self.dict[key][1][lang] = PhotoImage(file=filename)
        
    def __loadKeys(self, keyfile):
        """ initializes self.dict and returns keys
        """
        FILE = open(keyfile, "r")
        keys = FILE.readlines()
        FILE.close()

        r = []
        for key in keys:
            key = key.strip()
            r.append(key)
            if key == "":
                continue
            self.dict[key] = [{}, {}]

        return r
            
    def __loadDicts(self, filename):
        if filename == "":
            return []
        
        FILE = open(filename, "r")
        lines = FILE.readlines()
        FILE.close()
        
        r = []

        for line in lines:
            line = line.strip()

            if line == "":
                continue

            line_as_list = line.split(";")

            r.append([line_as_list[0], line_as_list[1]])

        return r
        
    def getWord(self, key, lang):

        try:
            word = self.dict[key][0][lang] # texts
        except KeyError:
            try:
                word = self.dict[key][1][lang] # images
            except KeyError:
                word = None

        return word
        
    def __loadTextDictFile(self, filename):
        """ file is in format key;word
            method returns a dictionary in format { "key" = "word", ... } """

        FILE = open(filename, "r")
        lines = FILE.readlines()
        FILE.close()
        
        r = {}

        for line in lines:
            line = line.strip()

            if line == "":
                continue
            
            line_as_list = line.split(";")
            r[line_as_list[0]] = line_as_list[1]

        return r
            
    def __loadHighlights(self, filename="highlights.csv", imagepath="images/highlights/"):
        if filename == "":
            return
        
        FILE = open(filename, "r")
        lines = FILE.readlines()
        FILE.close()

        for key in lines:
            key = key.strip()

            if key == "":
                continue

            giffile = imagepath + key + ".gif"

            self.highlight_images[key] = []
            self.highlight_images[key].append(PhotoImage(file=giffile))
            #the image is positioned outside the visible area
            image_id = self.canvas.create_image(0,0,
                                                image=self.highlight_images[key][0],
                                                anchor=S+E)
            self.highlight_images[key].append(image_id)

    def hiLiOn(self, key):
        image_id = self.highlight_images[key][1]

        self.canvas.itemconfigure(image_id, anchor=N+W)

    def hiLiOff(self, key):
        image_id = self.highlight_images[key][1]

        self.canvas.itemconfigure(image_id, anchor=S+E)

    def __setRegionEvents(self):
        for key, x in self.regions.iteritems():
            def handler(event, self=self, key=key):
                return self.__enterRegionEvent(event, key)
            self.canvas.tag_bind(key, "<Enter>", handler)

    def __enterRegionEvent(self, event, region_key):
        pass
    
    def __init__(self, bg_image=None, map_filename=None, master=None):
        
        Frame.__init__(self, master)
        self.createStuff(bg_image, map_filename)

        
if __name__ == '__main__':
    app = WICFrame()
    app.mainloop()



        
