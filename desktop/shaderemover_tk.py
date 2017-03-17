from tkinter import Tk, Frame, Menu, filedialog
from tkinter import Button, LEFT, TOP, X, FLAT, RAISED

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import sys

import numpy as np
import scipy.misc as misc
from skimage import transform
from PIL import Image, ImageOps
import math

from separateTVAndL1 import *



class Main(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        self.is_opened = False
        self.initUI()
        
        
    def initUI(self):

        # tkinter
        self.parent.title("Toolbar")
        
        toolbar = Frame(self.parent, bd=1, relief=RAISED)

        open_button = Button(toolbar, text="open", relief=FLAT,
            command=self.openFile)
        open_button.pack(side=LEFT, padx=2, pady=2)
        
        save_button = Button(toolbar, text="save", relief=FLAT,
            command=self.saveFile)
        save_button.pack(side=LEFT, padx=2, pady=2)
       
        toolbar.pack(side=TOP, fill=X)

        # matplotlib
        self.fig = plt.figure()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.ax = self.fig.add_subplot(111)
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=1)

        self.canvas._tkcanvas.pack(side="top", fill="both", expand=1)
        self.pack()

        im_raw = Image.open("opening.jpg")
        gray_img = ImageOps.grayscale(im_raw)
        gray_img = np.array(gray_img)
        gray_img = gray_img / 255.0
        self.ims = self.ax.imshow(gray_img, cmap="gray", vmin=0, vmax=1);

       
    def onExit(self):
        self.quit()

    def openFile(self):

        filepath = filedialog.askopenfilename()
        print(filepath)
        if filepath:
            pass
        else:
            print("No file selected")
            return
        
        try:
            im_raw = Image.open(filepath)
        except:
            print("Cannot Open File")
            
            return
        
        if im_raw == None:
            print("Cannot Open File")
            return

        gray_img = ImageOps.grayscale(im_raw)
        gray_img = np.array(gray_img)
        gray_img = gray_img / 255.0
        w_orig = gray_img.shape[1]
        h_orig = gray_img.shape[0]
        
        self.shadeless = removeShade(gray_img, 100)

        # make small image for preview
        if w_orig >= h_orig and w_orig > 1000:
            self.preview = transform.resize(self.shadeless, (math.floor(1000*h_orig/w_orig), 1000))
        elif h_orig >= w_orig and h_orig > 1000:
            self.preview = transform.resize(self.shadeless, (1000, math.floor(1000*w_orig/h_orig)))
        else:
            self.preview = np.array(self.shadeless)
        
        self.ims.set_data(self.preview);
        
        try:
            self.canvas.draw()
        except:
            print("Unexpected error:" + str(sys.exc_info()[0]))
            self.is_opened = False

        self.is_opened = True
        print("Completed")

    def saveFile(self):
        if not self.is_opened:
            return
        
        filepath = filedialog.asksaveasfilename()
        if filepath:
            pass
        else:
            print("No file selected")
            return
        try:
            plt.imsave(filepath, self.shadeless, cmap='gray', vmin=0, vmax=1)
        except:
            print("Unexpected error:" + str(sys.exc_info()))
        print("saved")
    

if __name__ == '__main__':
    root = Tk()
    root.geometry("600x400+300+300")
    app = Main(root)
    root.mainloop()  





    











    
    
