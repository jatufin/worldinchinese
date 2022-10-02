#!/usr/bin/python
###################################################
# World in Chinese
# (c) 2007 Janne Tuukkanen
###################################################
from Tkinter import *
import os

from pywic import wicstudyframe, wicselectregion, wicconnectors, wicselectword

global WIC_WIDTH, WIC_HEIGHT, WIC_BG_COLOR, WIC_TITLE
WIC_WIDTH = 800
WIC_HEIGHT = 600
WIC_BG_COLOR = "#ffe7b6"
WIC_TITLE = "World in Chinese"

global wic_root_dir, wic_work_dir, app_frame
app_frame = None

#wic_root_dir = wic_work_dir = os.getcwd()
wic_root_dir = wic_work_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(wic_work_dir)
        
class WICMainButtons(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, bg=WIC_BG_COLOR)

        #self.grid()

        self.goto_buttons = {}
        self.active_unit = None
        
        self.createStuff()

    def createStuff(self):
        self.logo_image = PhotoImage(file="images/logo.gif")
        self.logo = Canvas(self, width=440, height=200,
                           bg=WIC_BG_COLOR, highlightthickness=0)
        self.logo.create_image(0, 0, image=self.logo_image, anchor=N+W)
        self.logo.grid(column=0, row=0, columnspan=5)

        self.connect_label_0 = Label(self, text="Select unit:",
                                     bg=WIC_BG_COLOR)
        self.connect_label_0.grid(column=0, row=1,columnspan=3)

        self.createGoToButton("Regions of China", "china_regions/",
                              column=0, row=2)        
        self.createGoToButton("Chinese cities", "china_cities/",
                              column=0, row=3)        
        self.createGoToButton("Geography of China", "china_geography/",
                              column=0, row=4)        

        self.createGoToButton("European countries", "europe_countries/",
                              column=1, row=2)
        self.createGoToButton("East Asian countries", "east_asian_countries/",
                              column=1, row=3)
        self.createGoToButton("Countries in Middle East",
                              "middle_east_countries/",
                              column=1, row=4)
        self.createGoToButton("African countries",
                              "african_countries/",
                              column=1, row=5)
        self.createGoToButton("North American countries",
                              "north_america_countries/",
                              column=1, row=6)
        self.createGoToButton("South American countries",
                              "south_america_countries/",
                              column=1, row=7)
        self.createGoToButton("States of the US",
                              "us_states/",
                              column=1, row=8)

        self.createGoToButton("Continents and oceans",
                              "continents_oceans/",
                              column=2, row=2)

        self.createGoToButton("World geography",
                              "globe_geo/",
                              column=2, row=3)


        self.blank_label_0 = Label(self, text="", width=10, height=2,
                                   bg=WIC_BG_COLOR)
        self.blank_label_0.grid(column=3, row=1)

        self.connect_label_0 = Label(self, text="Select exercise:",
                                     bg=WIC_BG_COLOR)
        self.connect_label_0.grid(column=4, row=1)

        
        self.createFunctionButtons()

        self.disableFunctionButtons()
            
    def createGoToButton(self, text, directory, column=0, row=0, width=20):

        b = Button(self, text=text, bg=WIC_BG_COLOR, width=width,
                   activebackground=WIC_BG_COLOR,
                   highlightthickness=0, relief=FLAT)

        if not os.access(directory, os.F_OK):
            b.configure(state=DISABLED)
        
        def clickHandler(d=directory, button=b):
            self.buttonClickEvent(d, b)

        b["command"] = clickHandler
        
        self.goto_buttons[text] = b

        b.grid(column=column, row=row)

    def buttonClickEvent(self, d, button):
        global wic_work_dir
        
        if(self.active_unit != None):
            self.active_unit["relief"] = FLAT

        button["relief"] = GROOVE

        self.active_unit = button

        self.enableFunctionButtons()

        wic_work_dir = d
        
    def createFunctionButtons(self, column=4, row=2, width=20):
        i = row

        self.browse_button = Button(self, text="Browse places",
                                    bg=WIC_BG_COLOR, width=width,
                                    activebackground=WIC_BG_COLOR,
                                    command=self.browseHandler)
        self.browse_button.grid(column=column, row=i)
        i += 1
        self.select_button = Button(self, text="Match names",
                                    bg=WIC_BG_COLOR, width=width,
                                    activebackground=WIC_BG_COLOR,
                                    command=self.selectHandler)
        self.select_button.grid(column=column, row=i)
        i += 1
        self.select_word_button = Button(self, text="Select word",
                                         bg=WIC_BG_COLOR, width=width,
                                         activebackground=WIC_BG_COLOR,
                                         command=self.selectWordHandler)
        self.select_word_button.grid(column=column, row=i)
        i += 1 
        self.connect_label = Label(self, text="Connect words:",
                                   bg=WIC_BG_COLOR, width=width,
                                   activebackground=WIC_BG_COLOR)
        self.connect_label.grid(column=column, row=i)
        i += 1 
        def conHandler1(lang1="English", lang2="Pinyin"):
            self.connectHandler(lang1, lang2)
        self.connect_button_1 = Button(self, text="English to Pinyin",
                                       bg=WIC_BG_COLOR, width=width,
                                       activebackground=WIC_BG_COLOR,
                                       command=conHandler1)
        self.connect_button_1.grid(column=column, row=i)
        i += 1 
        def conHandler2(lang1="English", lang2="Simplified Chinese"):
            self.connectHandler(lang1, lang2)                
        self.connect_button_2 = Button(self, text="English to Simplified",
                                       bg=WIC_BG_COLOR, width=width,
                                       activebackground=WIC_BG_COLOR,
                                       command=conHandler2)
        self.connect_button_2.grid(column=column, row=i)
        i += 1 
        def conHandler3(lang1="English", lang2="Traditional Chinese"):
            self.connectHandler(lang1, lang2)                
        self.connect_button_3 = Button(self, text="English to Traditional",
                                       bg=WIC_BG_COLOR, width=width,
                                       activebackground=WIC_BG_COLOR,
                                       command=conHandler3)
        self.connect_button_3.grid(column=column, row=i)
        i += 1 
        def conHandler4(lang1="Pinyin", lang2="Simplified Chinese"):
            self.connectHandler(lang1, lang2)                
        self.connect_button_4 = Button(self, text="Pinyin to Simplified",
                                       bg=WIC_BG_COLOR, width=width,
                                       activebackground=WIC_BG_COLOR,
                                       command=conHandler4)
        self.connect_button_4.grid(column=column, row=i)
        i += 1 
        def conHandler5(lang1="Pinyin", lang2="Traditional Chinese"):
            self.connectHandler(lang1, lang2)                
        self.connect_button_5 = Button(self, text="Pinyin to Traditional",
                                       bg=WIC_BG_COLOR, width=width,
                                       activebackground=WIC_BG_COLOR,
                                       command=conHandler5)
        self.connect_button_5.grid(column=column, row=i)

    def enableFunctionButtons(self, state=NORMAL):
        self.browse_button.configure(state=state)
        self.select_button.configure(state=state)
        self.select_word_button.configure(state=state)
        self.connect_button_1.configure(state=state)
        self.connect_button_2.configure(state=state)
        self.connect_button_3.configure(state=state)
        self.connect_button_4.configure(state=state)
        self.connect_button_5.configure(state=state)


    def disableFunctionButtons(self,):
        self.enableFunctionButtons(state=DISABLED)
        
    def browseHandler(self):
        global app_frame, wic_work_dir

        os.chdir(wic_work_dir)
        
        app_frame = wicstudyframe.WICStudyFrame(master=self.master)
        app_frame.setLanguages("English", "Simplified Chinese",
                               "Traditional Chinese", "Pinyin")

        self.quit()

    def selectHandler(self):
        global app_frame, wic_work_dir
        
        os.chdir(wic_work_dir)

        app_frame = wicselectregion.WICSelectRegion(master=self.master)

        self.quit()


    def selectWordHandler(self):
        global app_frame, wic_work_dir
        
        os.chdir(wic_work_dir)

        app_frame = wicselectword.WICSelectWord(master=self.master)

        self.quit()

    def connectHandler(self, lang1, lang2):
        global app_frame, wic_work_dir

        os.chdir(wic_work_dir)

        app_frame = wicconnectors.WICConnectors(master=self.master,
                                                lang1=lang1, lang2=lang2)
        self.quit()


class WICMainFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master,
                       width=WIC_WIDTH, height=WIC_HEIGHT,
                       bg=WIC_BG_COLOR)
    
        self.master.title(WIC_TITLE)
        self.master.geometry("%dx%d+0+0" % (WIC_WIDTH, WIC_HEIGHT))
        self.master.minsize(WIC_WIDTH, WIC_HEIGHT)
        self.master.configure(bg=WIC_BG_COLOR)

        self.buttons = WICMainButtons(self)
        self.appframe = None
        
if __name__ == "__main__":
    root = Tk()

    global exit_status
    exit_status = False

    def rootExit():
        global exit_status
        exit_status = True
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", rootExit)

    main_app = WICMainFrame(root)
    main_app.pack()
    app_frame = None

    while(not exit_status):
        if app_frame == None:
            os.chdir(wic_root_dir)
            main_app.buttons.place(relx=0.5, rely=0.5, anchor=CENTER)
            main_app.mainloop()
        else:
            main_app.buttons.pack_forget()
            main_app.appframe = app_frame
            app_frame = None
            main_app.appframe.place(relx=0.5, rely=0.5, anchor=CENTER)
            main_app.appframe.mainloop()
            if(not exit_status):
                main_app.appframe.destroy()


            
