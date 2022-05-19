from operator import index

from click import command
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
simpath = os.path.abspath('')

axis = ["x", "y", "z"]
coils = []
coils_names = []
spinners = []
spinners_names = ["None"]

coil_counter = 0


class Designer(tk.Tk):

    def __init__(self):
        super().__init__()
        self.initial_window()
        self.geometry("800x600")

    def initial_window(self) -> None:

        global coils, coils_names, projectpath

        #Clean Frame
        for widget in self.winfo_children():
            widget.destroy()

        self.title("Designer")

        menubar = tk.Menu(self)
        self.config(menu=menubar)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.new_project)
        filemenu.add_command(label="Open", command=self.open_project)
        filemenu.add_command(label="Save", command=self.save_project)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Manual")

        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.path_text = tk.StringVar()
        self.path_lbl = tk.Label(self, text="Working directory: " + projectpath)
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
                 text= "Radius:").place(x=570,y=220)
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

        global projectpath, coils, coils_names, coil_counter

        path = filedialog.askdirectory(title= "Open project folder")

        if path:
            #Updating the path label
            projectpath = os.path.abspath(path)

            coils = []
            coils_names = []

            coil_counter = 0

            self.initial_window()

        self.load_project()

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

        global coils, coils_names, coil_counter, projectpath

        new_path = self.entry.get()

        os.mkdir(new_path)
        path = filedialog.askdirectory(title="Select the new project folder")

        if path:    
            #Updating the path label
            projectpath = os.path.abspath(path)
            
            coils = []
            coils_names = []

            coil_counter = 0

        self.initial_window()
        self.window.destroy()

    def save_project(self):

        global projectpath, coils

        #Creates project save if it does not exist
        if os.path.exists(projectpath + "/projectSave.txt"):
            #Erase previous save
            open(projectpath + "/projectSave.txt", "w").close()

        with open(projectpath + "/projectSave.txt", 'w') as file:
            for coil in coils:
                file.write("StartCoil")
                file.write("\n")
                vectors = coil.get_vectors()
                for vector in vectors:
                    file.write(str(vector[0]))
                    file.write(', ')
                    file.write(str(vector[1]))
                    file.write("\n")
                file.write("EndCoil")
                file.write("\n")

    def load_project(self):

        global coils, coils_names, coil_counter, projectpath

        with open(projectpath + "/projectSave.txt", 'r') as file:
            lines = file.readlines()
        
        cables_counter = 0
        
        for line in lines:
            line = line.replace('\n', '')

            if line == "StartCoil":
                cables = []
            elif line == "EndCoil":
                coils.append(sp.Coil(cables))
                coils_names.append("Coil " + str(coil_counter))
                coil_counter += 1
            else:
                c_list = lines[cables_counter].split(',')
                h_list = c_list[0].split(';')
                t_list = c_list[1].split(';')
                cables.append(sp.Cable(
                                       sp.Vector(float(h_list[0]),
                                                 float(h_list[1]),
                                                 float(h_list[2])),
                                       sp.Vector(float(t_list[0]),
                                                 float(t_list[1]),
                                                 float(t_list[2])),
                                       1))
            cables_counter += 1

        self.coils_menu = tk.OptionMenu(self,
                                   self.menu_var,
                                   *coils_names,
                                   command=self.set_coil)
        self.coils_menu.place(x=580, y=110, width= 100)
        
        self.menu_var.set(coils_names[len(coils)-1])
        self.plot_image()

    def create_polygon(self):
        
        global coils, coils_names, coil_counter

        coils_names.append("Coil " + str(coil_counter))
        self.coils_menu.destroy()
        self.coils_menu = tk.OptionMenu(self,
                                   self.menu_var,
                                   *coils_names,
                                   command=self.set_coil)
        self.coils_menu.place(x=580, y=110, width= 100)

        self.menu_var.set(coils_names[len(coils)-1])

        coils.append(sp.coil_gen_circle(float(self.radious.get()),
                                        int(self.vertices.get())))
        coil_counter += 1

        self.plot_image()

    def create_coil(self):

        global coils, coils_names, coil_counter

        coils_names.append("Coil " + str(coil_counter))
        self.coils_menu.destroy()
        self.coils_menu = tk.OptionMenu(self,
                                   self.menu_var,
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

    def set_coil(self, _):
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
        self.geometry("800x600")

    def initial_window(self) -> None:

        global coils, coils_names, simpath, spinners, spinners_names

        #Clean Frame
        for widget in self.winfo_children():
            widget.destroy()

        self.title("Simulator")

        menubar = tk.Menu(self)
        self.config(menu=menubar)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.new_sim)
        filemenu.add_command(label="Open", command=self.open_sim)
        filemenu.add_command(label="Save", command=self.save_sim)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Manual")

        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.path_text = tk.StringVar()
        self.path_lbl = tk.Label(self, text="Simulation: " + simpath)
        self.path_lbl.place(x=20, y=20)


        self.spin_var = []
        self.spin_menu = []

        tk.Label(self, text="Fix into").place(x=100, y=70)
        for i in range(len(coils_names)):
            tk.Label(self, text=coils_names[i]).place(x=20, y=90+40*i)
            self.spin_var.append(tk.StringVar(self))
            self.spin_var[i].set("None")
            self.spin_menu.append(tk.OptionMenu(self,
                                                self.spin_var[i],
                                                *spinners_names))
            self.spin_menu[i].place(x=80, y=85+40*i, width= 100)

        tk.Button(self, text="Start").place(x=710, y=45)


        ############################################################

        self.sim_frame = tk.Frame(self, width=520,height=180)
        self.sim_frame.config(relief="sunken", bd=5)
        self.sim_frame.place(x=250, y=80)

        tk.Label(self, text="**Simulation setings**").place(x=268, y=90)
        self.simtime_var = "0.1"
        tk.Label(self,
                 text= "sim time:").place(x=270,y=120)
        self.simtime = tk.Entry(self, width=8)
        self.simtime.insert(0, "0.1")
        tk.Label(self,
                 text= "seconds").place(x=350,y=140)
        self.simtime.place(x=270,y=140)
        self.step_var = "0.0005"
        tk.Label(self,
                 text= "time step:").place(x=270,y=160)
        self.step = tk.Entry(self, width=8)
        self.step.insert(0, "0.0005")
        tk.Label(self,
                 text= "seconds").place(x=350,y=180)
        self.step.place(x=270,y=180)

        self.video_var = tk.IntVar(self)
        self.csv_var = tk.IntVar(self)

        self.video_check = tk.Checkbutton(self,
                                          text="Video",
                                          variable=self.video_var,
                                          onvalue=1,
                                          offvalue=0)
        self.video_check.place(x=700,y=90)
        self.csv_check = tk.Checkbutton(self,
                                        text="CSV",
                                        variable=self.csv_var,
                                        onvalue=1,
                                        offvalue=0)
        self.csv_check.place(x=700,y=110)

        self.bfield_var = "0.0, 0.0, 0.007"
        tk.Label(self,
                 text= "B field: (x, y, z) T").place(x=470,y=120)
        self.bfield = tk.Entry(self, width=12)
        self.bfield.insert(0, "0.0, 0.0, 0.007")
        self.bfield.place(x=470,y=140)

        ############################################################

        self.coilsig_frame = tk.Frame(self, width=220,height=260)
        self.coilsig_frame.config(relief="sunken", bd=5)
        self.coilsig_frame.place(x=250, y=280)

        tk.Label(self, text="**Coil signals**").place(x=268, y=290)

        self.coil_sel_var = tk.StringVar(self)
        self.coil_sel_menu = tk.OptionMenu(self,
                                   self.coil_sel_var,
                                   *coils_names,
                                   command=self.change_coil)
        self.coil_sel_menu.place(x=360, y=315, width= 100)
        self.coil_sel_var.set("None")

        tk.Label(self, 
                 text= "frec:").place(x=268,y=330)
        self.frec = tk.Entry(self, width=8)
        self.frec.insert(0, "50")
        tk.Label(self,
                 text= "Hz").place(x=350,y=350)
        self.frec.place(x=270,y=350)
        tk.Label(self,
                 text= "start time:").place(x=270,y=370)
        self.start = tk.Entry(self, width=8)
        self.start.insert(0, "0.0")
        tk.Label(self,
                 text= "seconds").place(x=350,y=390)
        self.start.place(x=270,y=390)
        tk.Label(self, 
                 text= "Amplitude:").place(x=268,y=410)
        self.amp = tk.Entry(self, width=8)
        self.amp.insert(0, "50")
        tk.Label(self,
                 text= "A").place(x=350,y=430)
        self.amp.place(x=270,y=430)
        tk.Label(self, 
                 text= "Duty cycle:").place(x=268,y=450)
        self.duty = tk.Entry(self, width=8)
        self.duty.insert(0, "50")
        tk.Label(self,
                 text= "%").place(x=350,y=470)
        self.duty.place(x=270,y=470)

        self.sine_var = tk.IntVar(self)

        self.sine_check = tk.Checkbutton(self,
                                          text="Sine wave",
                                          variable=self.sine_var,
                                          onvalue=1,
                                          offvalue=0)
        self.sine_check.place(x=270,y=500)

        tk.Button(self, text="Save", command=self.savecoil).place(x=400, y=500)
        
        ############################################################

        self.spin_frame = tk.Frame(self, width=220,height=260)
        self.spin_frame.config(relief="sunken", bd=5)
        self.spin_frame.place(x=540, y=280)

        tk.Label(self, text="**Spinner setings**").place(x=550, y=290)
        self.spinner_sel_var = tk.StringVar(self)
        self.spinner_sel_menu = tk.OptionMenu(self,
                                   self.spinner_sel_var,
                                   *spinners_names,
                                   command=self.change_spinner)
        self.spinner_sel_menu.place(x=650, y=315, width= 100)
        self.spinner_sel_var.set("None")

        self.axpos_save = []
        tk.Label(self, 
                 text= "Axis position: (x, y, z)").place(x=545,y=410)
        self.axpos = tk.Entry(self, width=12)
        self.axpos.insert(0, "0.0, 0.0, 0.0")
        self.axpos.place(x=550,y=430)
        self.axdir_save = []
        tk.Label(self,
                 text= "Axis direction: (x, y, z)").place(x=545,y=450)
        self.axdir = tk.Entry(self, width=12)
        self.axdir.insert(0, "0.0, 0.0, 1.0")
        self.axdir.place(x=550,y=470)

        tk.Button(self, text="Add new", command=self.add_spinner).place(x=550, y=320)
        tk.Button(self, text="Del last", command=self.del_spinner).place(x=550, y=350)
        tk.Button(self, text="τ vs θ").place(x=680, y=500)
        tk.Button(self, text="Save", command=self.savespin).place(x=600, y=500)
        ############################################################

        self.frec_save = []
        self.start_save = []
        self.amp_save = []
        self.duty_save = []
        self.sine_save = []
        for _ in coils:
            self.frec_save.append(self.frec.get())
            self.start_save.append(self.start.get())
            self.amp_save.append(self.amp.get())
            self.duty_save.append(self.duty.get())
            self.sine_save.append(self.sine_var.get())


    
    def open_sim(self):

        global simpath, coils, coils_names, coil_counter

        path = filedialog.askdirectory(title= "Open simulation folder")

        if path:
            #Updating the path label
            simpath = os.path.abspath(path)

            self.initial_window()

        self.load_sim()

    def new_sim(self):

        global simpath

        self.window = tk.Tk()
        self.window.title("New simulation")

        tk.Label(self.window, 
                 text= "Write the new simulation's name:").pack(side=tk.TOP, 
                                                padx=200,
                                                pady=50)

        self.entry = tk.Entry(self.window)
        self.entry.insert(0, "NewSim")
        self.entry.pack(side = tk.TOP,
                padx=200,
                pady=50)

        tk.Button(self.window, text="Ok",
                command=self.ask_return).pack(side=tk.TOP,
                                                    pady=20,
                                                    padx=10)

        self.window.mainloop()

    def ask_return(self):

        global simpath, projectpath

        new_path = self.entry.get()

        os.mkdir(projectpath + "/" + new_path)
        path = filedialog.askdirectory(title="Select the new simulation's folder")

        if path:    
            #Updating the path label
            simpath = os.path.abspath(path)

        self.initial_window()
        self.window.destroy()

    def save_sim(self):

        global projectpath, coils

        #Creates project save if it does not exist
        if os.path.exists(simpath + "/simParameters.txt"):
            #Erase previous save
            open(simpath + "/simParameters.txt", "w").close()

        with open(simpath + "/simParameters.txt", 'w') as file:
            file.write("StartCoil")
                
    def load_sim(self):

        global coils, coils_names, simpath

    def add_spinner(self):

        global spinners, spinners_names, coils

        spinners_names.append("Spinner" + str(len(spinners_names)-1))

        self.spinner_sel_menu.destroy()
        self.spinner_sel_menu = tk.OptionMenu(self,
                                   self.spinner_sel_var,
                                   *spinners_names,
                                   command=self.change_spinner)
        self.spinner_sel_menu.place(x=650, y=315, width= 100)
        self.spinner_sel_var.set(spinners_names[len(spinners_names)-1])

        for i in range(len(coils_names)):
            self.spin_menu[i].destroy()

        self.spin_menu = []

        for i in range(len(coils_names)):
            self.spin_menu.append(tk.OptionMenu(self,
                                                    self.spin_var[i],
                                                    *spinners_names))
            self.spin_menu[i].place(x=80, y=85+40*i, width= 100)

        self.axpos_save.append("0.0, 0.0, 0.0")
        self.axdir_save.append("0.0, 0.0, 1.0")   

    def del_spinner(self):

        global spinners, spinners_names

        if len(spinners_names) > 1:

            temp = spinners_names.pop()

            for i in range(len(coils_names)):
                self.spin_menu[i].destroy()

            self.spin_menu = []
        
            for i in range(len(coils_names)):
                if self.spin_var[i].get() == temp:
                    self.spin_var[i].set("None")
                self.spin_menu.append(tk.OptionMenu(self,
                                                    self.spin_var[i],
                                                    *spinners_names,
                                                    command=self.change_spinner))
                self.spin_menu[i].place(x=80, y=85+40*i, width= 100)
                


            self.spinner_sel_menu.destroy()
            self.spinner_sel_var.set(spinners_names[len(spinners_names)-1])
            self.spinner_sel_menu = tk.OptionMenu(self,
                                    self.spinner_sel_var,
                                    *spinners_names)
            self.spinner_sel_menu.place(x=650, y=315, width= 100)

            self.axpos_save.pop()
            self.axdir_save.pop()   
            
    def savecoil(self):

        global coils, coils_names

        indx = coils_names.index(self.coil_sel_var.get())

        self.frec_save[indx] = self.frec.get()
        self.start_save[indx] = self.start.get()
        self.amp_save[indx] = self.amp.get()
        self.duty_save[indx] = self.duty.get()
        self.sine_save[indx] = self.sine_var.get()

    def savespin(self):
        
        global spinners, spinners_names

        indx = spinners_names.index(self.spinner_sel_var.get())

        self.axpos_save[indx-1] = self.axpos.get()
        self.axdir_save[indx-1] = self.axdir.get()
            
    def change_coil(self, coil):

        global coils, coils_names

        indx = coils_names.index(coil)

        self.frec.delete(0, 'end')
        self.frec.insert(0, self.frec_save[indx])
        self.start.delete(0, 'end')
        self.start.insert(0, self.start_save[indx])
        self.amp.delete(0, 'end')
        self.amp.insert(0, self.amp_save[indx])
        self.duty.delete(0, 'end')
        self.duty.insert(0, self.duty_save[indx])
        self.sine_var.set(self.sine_save[indx])

    def change_spinner(self, spinner):

        global spinners, spinners_names

        indx = spinners_names.index(spinner)

        self.axpos.delete(0, 'end')
        self.axpos.insert(0, self.axpos_save[indx-1])
        self.axdir.delete(0, 'end')
        self.axdir.insert(0, self.axdir_save[indx-1])


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
