###################################################
# World in Chinese
# (c) 2007 Janne Tuukkanen
###################################################
from Tkinter import *

class Bubble:
    """ Bubble enhancement for the Canvas widget"""
    
    def __create_coords(self, x, y, w, h, thickness, orientation):
        """Create bubble coordinates
        
           Creates coordinates for the bubble andreturns
           them in a list. First two items are x and y of
           the bubble's pointer

           Also declares __onActiveArea method for testing
           if pointer is pointed to allowed zone

           For instance, orientation 'south':

             x,y---------------------x1,y
             |                          |
             |                          |
             |                          |
             |        coords[0:3]       |
             |         x_mid,y2         |
             |            |             |
             x,y1-------------------x1,y1    <--- below this line (Y > y1)
                       |     |                    is the allowed zone
               x_mid-t/2     x_mid+t/2            for pointer
        """

        self.__fuzzy_dx, self.__fuzzy_dy = 0, 0
        FUZZINESS = 5
        t = thickness/2

        x_mid = x + w/2
        y_mid = y + h/2
        
        x1 = x + w
        y1 = y + h

        # we position the text in the middle of the bubble
        self.__text_x = x_mid
        self.__text_y = y_mid
        
        if orientation == 'north':
            # these lambdas are for checking, that bubble
            # pointer never crosses the pubble itself
            self.__onActiveArea = lambda _x,_y: _y < y 
            self.__fuzzy_dy = FUZZINESS
            self.__coords = [x_mid, y, x_mid, y, # sharp point if smooth=1
                             x_mid + t, y,
                             x1,y, x1,y1, x,y1, x,y,
                             x_mid - t, y]
            return

        if orientation == 'south':
            self.__onActiveArea = lambda _x,_y: _y > y1
            self.__fuzzy_dy = FUZZINESS * -1
            self.__coords = [x_mid, y1, x_mid, y1,
                             x_mid + t, y1,
                             x1,y1, x1,y, x,y, x,y1,
                             x_mid - t, y1]
            return
        

        if orientation == 'east':
            self.__onActiveArea = lambda _x,_y: _x > x1
            self.__fuzzy_dx = FUZZINESS * -1
            self.__coords = [x1, y_mid, x1, y_mid,
                             x1, y_mid + t,
                             x1, y1, x,y1, x,y, x1,y,
                             x1, y_mid - t]

        if orientation == 'west':
            self.__onActiveArea = lambda _x,_y: _x < x
            self.__fuzzy_dx = FUZZINESS
            self.__coords = [x, y_mid, x, y_mid,
                             x, y_mid - t,
                             x,y, x1,y, x1,y1, x,y1,
                             x, y_mid + t]
            return


    def __onActiveArea(self, x, y):
        """ Tests if given coordinates are on allowed zone

            This method is actually constructed in
            __create_coords method as lambda expressions"""
        return True
        
    def __init__(self, canvas, x, y, width, height, thickness=20, orientation='south', text='', image=None, fill="", outline="black"):
        self.canvas = canvas
        self.__x, self.__y, self.__width, self.__height = x, y, width, height
        self.__active_area_x, self.__active_area_y = 0, 0
        self.__thickness = thickness
        self.__orientation = orientation
        self.__is_pointing = False
        self.__polygon_id = 0
        self.__text_id = 0
        self.text_x, self.text_y = 0, 0
        self.__image_id = 0
        self.image_x, self.image_y = x + width / 2, y + height / 2

        

        # these we need to avoid some undesired effects when
        # following mouse and using Enter/Leave events same
        # time. Ee don't want to point the bubble exactly
        # to the mouse. Values are dependent from the orientation
        # of the bubble (see __create_coords method)
        self.__fuzzy_dx, self.__fuzzy_dy = 0, 0
        self.__fuzzy = 0

        # set the bubble and text coordinates
        self.__create_coords(x,y,width,height,thickness,orientation)

        # create polygon
        self.__polygon_id =  canvas.create_polygon(self.__coords)
        self.polyConfig(fill=fill, outline=outline) # fill, outline etc. default values

        # create text
        self.__text_id = canvas.create_text(self.__text_x, self.__text_y, text=text)
        self.textConfig(width=width)
        
    def getPolygonId(self):
        """ Returns the polygon id on the canvas"""
        
        return self.__polygon_id

    def tagRaise(self, tag):
        self.canvas.tag_raise(self.__polygon_id, tag)
        self.canvas.tag_raise(self.__text_id, self.__polygon_id)
        self.canvas.tag_raise(self.__image_id, self.__text_id)
        
    def pointTo(self, x, y):
        """ Point the bubble pointer to arguments"""
        
        x1 = self.__fuzzy * self.__fuzzy_dx + x
        y1 = self.__fuzzy * self.__fuzzy_dy + y

        # check if we are on the legal zone
        if(self.__onActiveArea(x1,y1) == False):
            return

        self.__coords[0] = self.__coords[2] = x1
        self.__coords[1] = self.__coords[3] = y1
        self.canvas.coords(self.__polygon_id, tuple(self.__coords))
        self.__is_pointing = True

    def stopPointing(self):
        """ Reset bubble pointer"""

        # Reset bubble back to rectangle
        self.__create_coords(self.__x, self.__y,
                             self.__width, self.__height,
                             self.__thickness,
                             self.__orientation)
        self.canvas.coords(self.__polygon_id, tuple(self.__coords))
        self.__is_pointing = False

    def isPointing(self):
        return self.__is_pointing
    
    def __pointToEventXY(self, event):
        self.pointTo(event.x, event.y)
        
    def followMouse(self):
        """ Start following mouse with bubble pointer

            It's NOT a good idea to connect more than one
            event handler to mouse motion (eg. other
            Bubbles)
            """

        self.__fuzzy = 1
        self.canvas.bind('<Motion>', self.__pointToEventXY)

    def stopFollowingMouse(self):
        """ Stop following mouse with bubble pointer

            Obs! This unbinds all <Motion> handlers
            from Canvas
            """

        self.__fuzzy = 0
        self.canvas.unbind('<Motion>')
        self.stopPointing()

    def toggleMouseFollow(self):
        """ Toggle between mouse follow modes"""

        if self.__is_pointing:
            self.stopFollowingMouse()
        else:
            self.__is_pointing = True # you need this
            self.followMouse()

    def setCoords(self, coords):
        self.canvas.coords(self.__polygon_id, tuple(coords))
        
    def polyConfig(self,
                   fill='',
                   outline='black',
                   stipple='',
                   width=1,
                   smooth=None,
                   tags=('bubble', 'bubble_poly')):
        """ Configure bubble polygon"""

        self.canvas.itemconfigure(self.__polygon_id, fill=fill,
                                    outline=outline, stipple=stipple,
                                    width=width, smooth=smooth, tags=tags)

    def getPolyConfig(self, option):
        return self.canvas.itemcget(self.__polygon_id, option)
    
    def textConfig(self,
                   anchor='center',
                   fill='black',
                   font=('Times','10'),
                   justify='left',
                   stipple='',
                   tags=('bubble', 'bubble_text'),
                   width=None):
        """ Configure bubble text"""

        self.canvas.itemconfigure(self.__text_id, anchor=anchor, fill=fill,
                                    font=font, justify=justify,
                                    stipple=stipple, tags=tags, width=width)

    def getTextConfig(self):
        return self.canvas.itemconfigure(self.__text_id)

    def setText(self, text):
        """ Set text value """

        self.canvas.itemconfigure(self.__text_id, text=text)
        
    def getText(self):
        """ Get text value """
        return self.canvas.itemcget(self.__text_id, 'text')

    def setImage(self, image):
        if  self.__image_id != 0:
            self.canvas.delete(self.__image_id)
        if image == None:
            return
        self.__image_id = self.canvas.create_image(self.image_x, self.image_y, image=image)

    def delImage(self):
        self.setImage(None)

    def setWord(self, word):
        if type(word) == str:
            self.delImage()
            self.setText(word)
            return
        self.setText("")
        self.setImage(word)

    def delWord(self):
        self.setText("")
        self.delImage()

    def getCoords(self):
        return self.__coords
        
    def bindEvent(self, event_string, function):
        """ Bind an event to bubble """
        
        # this inner function we need to provide actual
        # event handler 'self', current Bubble object
        def handler(event, function=function, self=self):
            function(event, self)
        self.canvas.tag_bind(self.__polygon_id, event_string, handler)
        self.canvas.tag_bind(self.__text_id, event_string, handler)
        
if __name__ == "__main__":
    active = None
    root = Tk()

    f = Frame()
    f.pack()

    f.winfo_toplevel().resizable(width=False, height=False)

    pohja = Canvas(f,width=500, height=400, bg='white')
    
    kupla = Bubble(pohja, 20,20,150,50, text="Foo")
    kupla.polyConfig(smooth=1)

    #img = PhotoImage(file="images/america.gif")
    #kupla.setImage(img)

    kupla.followMouse()
    
    pohja.pack()
    root.mainloop()


class MultiWordBubble(Bubble):
    def __init__(self, canvas, x, y, width, height, languages, thickness=20,
                 orientation='south', text='', image=None, buttons=False):
        
        Bubble.__init__(self, canvas, x, y, width, height, thickness,
                        orientation, text, image)

        self.enable_image = PhotoImage(file="images/enable.gif")
        self.disable_image = PhotoImage(file="images/disable.gif")
        self.words = {}

        dx = width / (len(languages) + 1)
        dy = height / 2
        i = 1
        
        for lang in languages:
            x1 = x + i * dx
            y1 = y + height/2
            button_y = y + height / 5
            i = i + 1
            self.words[lang] = {}
            self.words[lang]["enabled"] = True
            self.words[lang]["word"] = None
            self.words[lang]["text"] = self.canvas.create_text(x1, y1, font=("Times", 10))
            self.words[lang]["image"] = self.canvas.create_image(x1, y1)
            self.words[lang]["button"] = self.canvas.create_image(x1, button_y)
            if buttons:
                self.buttonOn(lang)
                def handler(event, lang=lang):
                    self.buttonEvent(event, lang)
                self.canvas.tag_bind(self.words[lang]["button"], "<Button-1>", handler)

    def buttonOn(self, lang):
        if self.words[lang]["enabled"]:
            self.canvas.itemconfigure(self.words[lang]["button"],
                                      image=self.disable_image)
            
        else:
            self.canvas.itemconfigure(self.words[lang]["button"],
                                      image=self.enable_image)

    def buttonOff(self, lang):
        self.canvas.itemconfigure(self.words[lang]["button"], image="")

    def setWord(self, lang, word):
        self.words[lang]["word"] = word
        if self.words[lang]["enabled"]:
            self.showWord(lang)
            
    def showWord(self, lang):
        word = self.words[lang]["word"]

        if word == None:
            return
        
        if type(word) == str:
            self.canvas.itemconfigure(self.words[lang]["text"],
                                      text=word)
        else:
            self.canvas.itemconfigure(self.words[lang]["image"],
                                      image=word)

    def hideWord(self, lang):
        self.canvas.itemconfigure(self.words[lang]["text"], text="")
        self.canvas.itemconfigure(self.words[lang]["image"], image="")
    
    def buttonEvent(self, event, lang):
        if self.words[lang]["enabled"]:
            self.words[lang]["enabled"] = False
            self.hideWord(lang)
        else:
            self.words[lang]["enabled"] = True
            self.showWord(lang)

        self.buttonOn(lang)
