# 3D Model Viewer in python

I "built" this tool to visualize 3D models and write and apply shaders to them. Specifically a Tesselation Shader for creating PN-Triangles. 
Most of the tesselation Code comes from https://ogldev.org/www/tutorial31/tutorial31.html. I only made slight modifications

For those further intrested in PN-Triangles i can recommend this Site: https://www.gamedeveloper.com/programming/b-zier-triangles-and-n-patches

They also provide a handful of resources for further reading


## Usage:

this Tool uses the following python libaries:
 - glfw
 - OpenGL
 - pyassimp
 - glm
 - ctypes
 - the time module from pygame

everyone of these can be installed via pip

to get started clone this repo with:

```
git clone https://github.com/hakrackete/3D-viewer.git
```

in the first lines of the 3Drenderer.py you can select the path to the Model. Only .obj models have been tested.
This Repo comes with a fine selection of Models such as Susanne or bunny_smol_richtig. some models do work, others do not. 

Specify one model and start the programm, you now have options:
 - [1-9] choose Tesselation Level
 - [T] toggle wireframe Modus
 - [L] illuminate Everything
 - [N,M] Scale the PN-Factor
 - [Arrow-Keys] change Rotation of the Model
 - [W,S] Zoom in/out 
 - [H] Print the Help screen

## how to use your own Models :))
  1. create a wonderful model in blender
  2. select shade smooth, (this is important otherwise the normals are not stor4ed per vertex, and we need that)
  3. export the model als .obj, make sure that in the export tab of blender the options Normals and Triangulate Mesh are enabled. Without these you might seen only half of the triangles
  4. move the .obj in the /models folder
  5. specify the name of the Model in the Python file
