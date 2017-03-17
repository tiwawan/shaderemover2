import matplotlib
import sys
matplotlib.rcParams['backend.qt5'] = 'PyQt5'
matplotlib.use('Qt5Agg')

import numpy as np
import scipy.misc as misc
from skimage import transform

import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QFileDialog, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap

from PIL import Image, ImageOps, ImageQt

import logging

from separateTVAndL1 import *

class Main(QMainWindow):
    
    def __init__(self):
        super(Main, self).__init__()
        self.is_opened = False
        self.image = None
        self.initUI()

    def initUI(self):
        # toolbars
        act_open = QAction("Open", self)
        act_open.triggered.connect(self.openFile)

        act_save = QAction("Save", self)
        act_save.triggered.connect(self.saveFile)

        self.toolbar = self.addToolBar('File')
        self.toolbar.addAction(act_open)
        self.toolbar.addAction(act_save)

        # pyplot figure
        
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)

        self.setCentralWidget(self.canvas)
        """
        self.lbl = QLabel(self)
        pixmap = QPixmap("../experimental/looseleaf_ss.jpg")
        self.lbl.setPixmap(pixmap)
        self.setCentralWidget(self.lbl)
        """
        im_raw = Image.open("opening.jpg")
        gray_img = ImageOps.grayscale(im_raw)
        gray_img = np.array(gray_img)
        gray_img = gray_img / 255.0
        self.ims = self.ax.imshow(gray_img, cmap="gray", vmin=0, vmax=1);

        self.show()
        
    def openFile(self):

        filepath = QFileDialog.getOpenFileName(self, 'Open file', './')
        
        if filepath[0]:
            pass
        else:
            print("No file selected")
            return
        
        try:
            im_raw = Image.open(filepath[0])
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
            self.preview = transform.resize(self.shadeless, (1000*h_orig/w_orig, 1000))
        elif h_orig >= w_orig and h_orig > 1000:
            self.preview = transform.resize(self.shadeless, (1000, 1000*w_orig/h_orig))
        else:
            self.preview = np.array(self.shadeless)
        
        self.ims.set_data(self.preview);
        
        try:
            self.canvas.draw();
        except:
            print("Unexpected error:" + str(sys.exc_info()[0]))

        self.is_opened = True
        print("Completed")

    def saveFile(self):
        filepath = QFileDialog.getSaveFileName(self, 'Open file', './')
        if filepath[0]:
            pass
        else:
            print("No file selected")
            return
        try:
            plt.imsave(filepath[0], self.shadeless, cmap='gray', vmin=0, vmax=1)
        except:
            print("Unexpected error:" + str(sys.exc_info()[0]))
        pass

    


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    m = Main()
    app.exec_()
    
    """
    im_raw = Image.open("../experimental/looseleaf_ss.jpg")
    gray_img = ImageOps.grayscale(im_raw)
    gray_img = np.array(gray_img)
    gray_img = gray_img / 255.0

    #S = removeShade(gray_img)

    ims = plt.imshow(im_raw, cmap="gray", vmin=0, vmax=1)
    ims.set_data(np.eye(100))
    plt.colorbar()
    plt.show()    """
    
    











    
    
