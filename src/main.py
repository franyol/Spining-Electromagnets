import modules.spining_electromagnets as sp
import modules.spining_simulator as ss

import os

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk


projectpath = os.path.abspath('')

axis = ["x", "y", "z"]
coils = []
coils_names = []

coil_counter = 0


class Designer(tk.Tk):

    def __init__(self):
        super().__init__()
        self.initial_window()
        self.geometry("800x600")

    def initial_window(self) -> None:

        global coils, coils_names

        self.title("Designer")

        menubar = tk.Menu(self)
        self.config(menu=menubar)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.new_project)
        filemenu.add_command(label="Open", command=self.open_project)
        filemenu.add_command(label="Save")
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Manual")

        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.path_text = tk.StringVar()
        self.path_lbl = tk.Label(self, text="Opened : No directory selected")
        self.path_lbl.place(x=20, y=20)

        self.img_frame = tk.Frame(self, width=520,height=370)
        self.img_frame.config(bg="gray", relief="sunken", bd=10)
        self.img_frame.place(x=20, y=80)

        self.editor_frame = tk.Frame(self, width=220,height=380)
        self.editor_frame.config(relief="sunken", bd=5)
        self.editor_frame.place(x=560, y=80)

        tk.Button(self, text="inspect", width= 7,
                command=self.inspect).place(x=25, y=45)

        tk.Button(self, text="Simulate",
                command=open_simulation).place(x=120, y=45)

        ##########################################################
        tk.Label(self, text="Coils").place(x=580, y=90)
        self.menu_var = tk.StringVar(self)
        self.coils_menu = tk.OptionMenu(self,
                                   self.menu_var,
                                   value="None",
                                   *coils_names)
        self.coils_menu.place(x=580, y=110, width= 100)

        ##########################################################
        tk.Label(self, text="Create").place(x=580, y=160)
        tk.Label(self, 
                 text= "Radious:").place(x=570,y=220)
        self.radious = tk.Entry(self, width=8)
        self.radious.insert(0, "0.03")
        self.radious.place(x=580,y=240)
        tk.Label(self, 
                 text="# of turns").place(x=670, y=220)
        self.turns = tk.Entry(self, width=8)
        self.turns.insert(0, "5")
        self.turns.place(x=680,y=240)
        tk.Label(self, 
                 text= "Cable diam:").place(x=570,y=260)
        self.diam = tk.Entry(self, width=8)
        self.diam.insert(0, "0.0003")
        self.diam.place(x=580,y=280)
        tk.Label(self, 
                 text="TurnsPerLayer").place(x=665, y=260)
        self.tpl = tk.Entry(self, width=8)
        self.tpl.insert(0, "5")
        self.tpl.place(x=680,y=280)
        tk.Label(self, 
                 text="Vertices").place(x=570, y=300)
        self.vertices = tk.Entry(self, width=8)
        self.vertices.insert(0, "20")
        self.vertices.place(x=580,y=320)
        tk.Button(self, text="polygon",
                command=self.create_polygon).place(x=580, y=180)
        tk.Button(self, text="coil", width= 7,
                command=self.create_coil).place(x=670, y=180)
        ##########################################################

        tk.Label(self, text="Edit").place(x=580, y=350)
        tk.Button(self, text="Move", width= 5,
                command=self.move).place(x=565, y=370)
        tk.Button(self, text="Rotate", width= 5,
                command=self.rotate).place(x=635, y=370)
        tk.Button(self, text="Delete", width= 5,
                command=self.delete).place(x=705, y=370)

        tk.Label(self, text="Axis").place(x=720, y=400)
        self.axis_var = tk.StringVar(self)
        self.axis_var.set("x")
        self.axis_menu = tk.OptionMenu(self,
                                   self.axis_var,
                                   *axis)
        self.axis_menu.place(x=720, y=420)

        tk.Label(self, 
                 text="Distance").place(x=570, y=400)
        self.dist = tk.Entry(self, width=8)
        self.dist.insert(0, "0.005")
        self.dist.place(x=570,y=420)

        tk.Label(self, 
                 text="Rad angle").place(x=650, y=400)
        self.angle = tk.Entry(self, width=8)
        self.angle.insert(0, "1.57")
        self.angle.place(x=650,y=420)

        



    def open_project(self):

        global projectpath

        path = filedialog.askdirectory(title= "Open project folder")

        if path:
            #Updating the path label
            projectpath = os.path.abspath(path)
            self.path_text.set("Working on: " + str(projectpath))
            self.path_lbl.config(textvariable=self.path_text)

    def new_project(self):

        global projectpath

        self.window = tk.Tk()
        self.window.title("New project")

        tk.Label(self.window, 
                 text= "Write the new project's name:").pack(side=tk.TOP, 
                                                padx=200,
                                                pady=50)

        self.entry = tk.Entry(self.window)
        self.entry.insert(0, "New Project(1)")
        self.entry.pack(side = tk.TOP,
                padx=200,
                pady=50)

        tk.Button(self.window, text="Ok",
                command=self.ask_return).pack(side=tk.TOP,
                                                    pady=20,
                                                    padx=10)

        self.window.mainloop()

    def ask_return(self):
        new_path = self.entry.get()

        os.mkdir(new_path)
        path = filedialog.askdirectory(title="Select the new project folder")

        if path:    
            #Updating the path label
            projectpath = os.path.abspath(path)
            self.path_text.set("Opened : " + str(projectpath))
            self.path_lbl.config(textvariable=self.path_text)

        self.window.destroy()

    def create_polygon(self):
        
        global coils, coils_names, coil_counter

        coils_names.append("Coil " + str(coil_counter))
        self.coils_menu.destroy()
        self.coils_menu = tk.OptionMenu(self,
                                   self.menu_var,
                                   coils_names[len(coils_names)-1],
                                   *coils_names,
                                   command=self.set_coil)
        self.coils_menu.place(x=580, y=110, width= 100)

        coils.append(sp.coil_gen_circle(float(self.radious.get()),
                                        int(self.vertices.get())))
        coil_counter += 1

        self.menu_var.set(coils_names[len(coils)-1])
        self.plot_image()

    def create_coil(self):

        global coils, coils_names, coil_counter

        coils_names.append("Coil " + str(coil_counter))
        self.coils_menu.destroy()
        self.coils_menu = tk.OptionMenu(self,
                                   self.menu_var,
                                   coils_names[len(coils_names)-1],
                                   *coils_names,
                                   command=self.set_coil)
        self.coils_menu.place(x=580, y=110, width= 100)

        coils.append(sp.coil_gen_coil(float(self.radious.get()),
                                      int(self.vertices.get()),
                                      int(self.turns.get()),
                                      int(self.tpl.get()),
                                      float(self.diam.get())))
        coil_counter += 1
        
        self.menu_var.set(coils_names[len(coils)-1])
        self.plot_image()

    def set_coil(self, option):
        self.plot_image()

    def plot_image(self):

        global projectpath, coils, coils_names

        #Creates cache dir if it does not exist
        if not os.path.exists(projectpath + "/cache"):
            os.mkdir(projectpath + "/cache")

        indx = coils_names.index(self.menu_var.get())

        plt.close('all')
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        for i in range(len(coils)):
            if i == indx:
                continue
            coils[i].plot(ax)

        coils[indx].plot(ax, 'red')

        plt.savefig(projectpath + "/cache/img.png")

        self.img_scaled = resize_image(cv.imread(projectpath + "/cache/img.png"))
        cv.imwrite('resized_image.png', self.img_scaled) 
        self.img = Image.open('resized_image.png')
        self.img = ImageTk.PhotoImage(self.img)

        self.editor_img = ttk.Label(self, image=self.img)
        self.editor_img.place(x=25, y=85)
        
    def move(self):
        
        global coils, coils_names

        indx = coils_names.index(self.menu_var.get())
        select_axis = self.axis_var.get()

        if(select_axis == "x"):
            coils[indx].move(sp.Vector(float(self.dist.get()), 0, 0))
        elif(select_axis == "y"):
            coils[indx].move(sp.Vector(0, float(self.dist.get()), 0))
        elif(select_axis == "z"):
            coils[indx].move(sp.Vector(0, 0, float(self.dist.get())))

        self.plot_image()

    def inspect(self):
        self.plot_image()
        plt.show()
        
    def rotate(self):

        global coils, coils_names

        indx = coils_names.index(self.menu_var.get())
        select_axis = self.axis_var.get()

        if(select_axis == "x"):
            r_axis = sp.RotationAxis(sp.Vector(0,0,0), sp.Vector(1,0,0))
        elif(select_axis == "y"):
            r_axis = sp.RotationAxis(sp.Vector(0,0,0), sp.Vector(0,1,0))
        elif(select_axis == "z"):
            r_axis = sp.RotationAxis(sp.Vector(0,0,0), sp.Vector(0,0,1))

        coils[indx].rotate(float(self.angle.get()), r_axis)

        self.plot_image()

    def delete(self):

        global coil_counter, coils, coils_names

        indx = coils_names.index(self.menu_var.get())

        coils.pop(indx)
        coils_names.pop(indx)

        self.coils_menu.destroy()
        self.coils_menu = tk.OptionMenu(self,
                                   self.menu_var,
                                   coils_names[len(coils_names)-1],
                                   *coils_names,
                                   command=self.set_coil)
        self.coils_menu.place(x=580, y=110, width= 100)

        self.menu_var.set(coils_names[len(coils)-1])
        self.plot_image()



class Simulation(tk.Tk):

    def __init__(self):
        super().__init__()
        self.initial_window()

    def initial_window(self) -> None:

        self.title("Simulation")

        tk.Button(self, 
                  text="Designer",
                  command=open_designer).pack(side=tk.LEFT,
                                              pady=20,
                                              padx=10)


def open_designer():
    window = Designer()
    window.mainloop()

def open_simulation():
    window = Simulation()
    window.mainloop()

def resize_image(img2scale: np.array) -> np.array:
    '''! Resize into visualizable dimentions'''

    dimensions = img2scale.shape

    width = 510
    height = 360
    return cv.resize(img2scale[60:dimensions[0]-30, 100:dimensions[1]-40], 
                     (width, height),
                     interpolation=cv.INTER_AREA)



open_designer()



"""
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

bobina = sp.coil_gen_coil(0.02, 4, 15, 5)

bobina.plot(ax)

plt.show()
"""
