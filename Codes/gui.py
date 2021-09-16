import tkinter as tk
from tkinter import *
import main_py
from tkinter import ttk

class Attributes:
    def __init__(self):
        pass

    def setVal(self, win_name, peds, cars, resoX, resoY, scale_factor, min_neighbour):
        self.win_name = win_name
        if peds == 1:
            self.peds = True
        elif peds == 0:
            self.peds = False

        if cars == 1:
            self.cars = True
        elif cars == 0:
            self.cars = False
        self.resoX = resoX
        self.resoY = resoY
        self.scale_factor = scale_factor
        self.min_neighbour = min_neighbour

    def printVal(self):
        print(self.win_name, self.peds, self.cars, self.resoX, self.resoY, self.scale_factor, self.min_neighbour)

params = Attributes()

class MyGui: 
    def __init__(self, name):
        self.window = tk.Tk()
        self.window.title(name)

        self.style = ttk.Style(self.window)
        #self.style.theme_use("scidgrey")

        self.window_name_entry = tk.StringVar() 
        self.window_label = tk.Label(self.window, text = "Window name :").grid(row = 0, column = 0, sticky = 'W')
        self.window_name_entry = tk.Entry(self.window)
        self.window_name_entry.grid(row = 0, column = 1)
        self.window_name_entry.insert(0, 'POCO F1')

        self.blank_label_1 = tk.Label(self.window, text = "",).grid(row = 1, column = 0)

        self.ped_var = IntVar()
        tk.Checkbutton(self.window, text = "Pedestrians", variable = self.ped_var ).grid(row = 2, column = 0, sticky = 'W')
        self.car_var = IntVar()
        tk.Checkbutton(self.window, text = "Cars       ", variable = self.car_var ).grid(row = 2, column = 1, sticky = 'W')

        self.blank_label_2 = tk.Label(self.window, text = "",).grid(row = 3, column = 0)

        self.resoX_entry = tk.IntVar()
        self.resoY_entry = tk.IntVar()
        self.reso_label = tk.Label(self.window, text = "Resolution : [Only integers] ").grid(row = 4, column = 0, sticky = 'W')
        self.resoX_entry = tk.Entry(self.window)
        self.resoX_entry.grid(row = 4, column = 1)
        self.resoX_entry.insert(0, '580')
        self.resoY_entry = tk.Entry(self.window)
        self.resoY_entry.grid(row = 4, column = 2)
        self.resoY_entry.insert(0, '280')

        self.blank_label_3 = tk.Label(self.window, text = "",).grid(row = 5, column = 0)
        
        self.scale_entry = tk.DoubleVar()
        self.scale_label = tk.Label(self.window, text = "Scale factor : [n > 1]").grid(row = 6, column = 0, sticky = 'W')
        self.scale_entry = tk.Entry(self.window)
        self.scale_entry.grid(row = 6, column = 1)
        self.scale_entry.insert(0, '1.05')

        self.neighbour_entry = tk.IntVar()
        self.neighbour_label = tk.Label(self.window, text = "Min Neighbours : ").grid(row = 7, column = 0, sticky = 'W')
        self.neighbour_entry = tk.Entry(self.window)
        self.neighbour_entry.grid(row = 7, column = 1)
        self.neighbour_entry.insert(0, '2')

        self.blank_label_4 = tk.Label(self.window, text = "",).grid(row = 8, column = 0)

        self.start_button = tk.Button(self.window, text = 'Start', width = 10, command = self.start).grid(row = 9, column = 0)
        

    def run(self):
        self.window.mainloop()

    
    def start(self):
        params.setVal(self.window_name_entry.get(), self.ped_var.get(), self.car_var.get(), self.resoX_entry.get(), self.resoY_entry.get(), self.scale_entry.get(), self.neighbour_entry.get())
        self.window.destroy()


def test():
    mygui = MyGui("Accident Prevention using OpenCV")
    mygui.run()
    params.printVal()
test()

main_py.setValues(params)


#have to do some multi threading
