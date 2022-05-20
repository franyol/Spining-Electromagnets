<h1 align="center">Spining-Electromagnets</h1>
<p align="center">
   <img src="https://user-images.githubusercontent.com/94434464/169480385-5ee39d04-f095-4238-9b4b-8fc7093d3711.gif">
</p>
If you are reading this you may need a tool for simulating the rotation of small electromagnets inside a constant magnetic field, if that's the case, this is your repo! If you just wanna see some coils spinning, you are also wellcome ;). With this project you can design/save/modify as many coils as you are capable of and then fix them into specific rotation axis an see the ressult.

***Here are the movement and torque graphs of the simulation you saw on the gif above:***

![image](https://user-images.githubusercontent.com/94434464/169485552-86ac1055-03e1-4be5-a56b-49fd782018fa.png)

# Table of Contents

1. [Requirements](#requirements)
2. [Creating our first project](#creating-our-first-project)
3. [Designer interface](#designer-interface)
4. [Simulator interface](#simulator-interface)
5. [Using the modules instead of the GUI](#using-the-modules-instead-of-the-gui)
6. [The physics behind this project](#the-physics-behind-this-project)

## Requirements
Make sure you have these dependencies latest versions installed:

- [Pillow](https://pillow.readthedocs.io/en/stable/installation.html)
- [opencv](https://pypi.org/project/opencv-python/)
- [tkinter](https://www.tutorialspoint.com/how-to-install-tkinter-in-python)
- [matplotlib](https://matplotlib.org/stable/users/installing/index.html)
## Creating our first project
Right after you have clonned the repo, you can run the GUI by typing ``` python3 src/main.py ``` on the command line. The dessigner window will show up. Before starting, be sure to change the working directory by clicking on "file" and then "new" for creating a new directory or "open" to load an existing one:

![image](https://user-images.githubusercontent.com/94434464/169494526-af04d844-df54-4b3e-aad7-ddd670a059a5.png)

I'm clickin on "new" so we can create a project from scratch.

Write the new directory's name: 

![image](https://user-images.githubusercontent.com/94434464/169494923-aee159d3-849e-4789-87db-8471d487aca9.png)

And now select the directory we just created (be sure to be insede it before clicking "ok"):

![image](https://user-images.githubusercontent.com/94434464/169495271-f1a662a2-a01f-4b59-88b8-b4780e1eaee4.png)

Now your current directory must be reflected on the top of the Designer interface window.

## Designer interface

Here is where we will create the coils/ Electromagets that will be spinning in this project:

![image](https://user-images.githubusercontent.com/94434464/169495692-6c883f94-f6ae-49e0-a033-56e566e4d8eb.png)

To create a new one, we can press on "Polygon" to create a single current loop, or clock on "Coil" to create an N looped Coil.

First, we will create a single-looped square "Polygon".
Set the parameters like this before clicking:

![image](https://user-images.githubusercontent.com/94434464/169497985-9c7568a9-84a1-425e-b825-4b0deb38fd67.png)
 
For a polygon we just have to set the "radius" and "Vertices" parameters.

Now there has appeared a new named "Coil 0" Coil on our selection menu! We can also see the coil we just created in the left side of the window:

![image](https://user-images.githubusercontent.com/94434464/169498637-f03cfc05-c263-4cbc-a4cd-d9f7474b9dca.png)

Now you can clock on the "Inspect" button to have a better look to the design anytime.
 
![image](https://user-images.githubusercontent.com/94434464/169498862-6c8c2b69-30bf-40bb-804a-0f661f7ffdf6.png)

We can move and rotate the Coil 0 we have created by selecting the axis we are moving on or rotating around, typing the angle in radians or the distance in meters and then pressing it's respective buttons:

![image](https://user-images.githubusercontent.com/94434464/169499598-f4e31e92-695b-4f0a-b274-4a339779c5da.png)

Rotate the coil in the z axis by this value:

![image](https://user-images.githubusercontent.com/94434464/169500092-8ffb3e71-3fac-4c60-83e2-a1aa372feb42.png)

Rotate it again in the x axis:

![image](https://user-images.githubusercontent.com/94434464/169500409-27f64843-98c1-4949-b175-ad9de4a59344.png)

Create another square polygon Coil and rotate it like this:

![image](https://user-images.githubusercontent.com/94434464/169500092-8ffb3e71-3fac-4c60-83e2-a1aa372feb42.png)
![image](https://user-images.githubusercontent.com/94434464/169500751-dadf20ff-4a68-4eae-9f05-bb1775eb8079.png)

You can change the coil you are editing in the Coil selection menu and see that coil coloring red:

![image](https://user-images.githubusercontent.com/94434464/169501041-1deebd50-ade5-49e8-98ee-756febc464ed.png)

Delete the selected Coil anytime by pressing on "Delete".

## Simulator interface
Some text.
## Using the modules instead of the GUI
Some text.
## The physics behind this project
Some text.
