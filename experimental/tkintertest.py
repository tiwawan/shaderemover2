from tkinter import Tk, Frame, Menu
from tkinter import Button, LEFT, TOP, X, FLAT, RAISED

import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
        
    def initUI(self):
      
        self.parent.title("Toolbar")
        
        toolbar = Frame(self.parent, bd=1, relief=RAISED)

        exitButton = Button(toolbar, text="exit", relief=FLAT,
            command=doing)
        exitButton.pack(side=LEFT, padx=2, pady=2)
       
        toolbar.pack(side=TOP, fill=X)

        f = plt.figure()
        a = f.add_subplot(111)
        canvas = FigureCanvasTkAgg(f, master=self)
        canvas.show()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=1)

        canvas._tkcanvas.pack(side="top", fill="both", expand=1)
        self.pack()
        
       
    def onExit(self):
        self.quit()


def main():
  
    root = Tk()
    root.geometry("600x400+300+300")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
