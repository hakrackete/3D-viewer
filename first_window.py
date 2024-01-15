import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader
import pyassimp


class App:
    def __init__(self):
        pg.init()
        pg.display.set_mode((400,400),pg.OPENGL|pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        glClearColor(0.1,0.2,0.2,1)
        self.shader = self.createShader("shaders/vertex.vert","shaders/fragment.frag")
        glUseProgram(self.shader)
        self.triangle = Triangle()
        self.mainLoop()

    def createShader(self,vertexFilepath,fragementFilepath):
        with open(vertexFilepath,"r")as f:
            vertex_src = f.readlines()
                
        with open(fragementFilepath,"r")as f:
            fragement_src = f.readlines()
        
        shader = compileProgram(
            compileShader(vertex_src,GL_VERTEX_SHADER),
            compileShader(fragement_src,GL_FRAGMENT_SHADER)
        )
        
        return shader

    def mainLoop(self):
        running = True
        while running:
            seconds_passed = pg.time.get_ticks()/1000
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
            
            
            glClear(GL_COLOR_BUFFER_BIT)

            glUniform1f( glGetUniformLocation( self.shader, 'time' ),seconds_passed)

            glUseProgram(self.shader)
            glBindVertexArray(self.triangle.vao)
            glDrawArrays(GL_TRIANGLES,0,self.triangle.vertexcount)

            pg.display.flip()
            self.clock.tick(60)
        self.quit()

    def quit(self):
        self.triangle.destroy()
        glDeleteProgram(self.shader)
        pg.quit()

class Triangle:
    def __init__(self):
        self.verticies = (
            -0.5,-0.5,0.0,1.0,0.0,0.0,
            0.5,-0.5,0.0,0.0,1.0,0.0,
            0.0,0.5,0.0,0.0,0.0,1.0
        )

        # wir brauche numpy, weil dies unsere floats in c-style 32bit floats umwandelt. wichtig für die gpu
        self.verticies = np.array(self.verticies,dtype=np.float32)
        self.vertexcount = 3

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER,self.vbo)
        glBufferData(GL_ARRAY_BUFFER,self.verticies.nbytes,self.verticies,GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(0))
        
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(12)) 

    def destroy(self):
        glDeleteVertexArrays(1,(self.vao,))
        glDeleteBuffers(1,(self.vbo,0))


if __name__ == "__main__":
    myApp = App()