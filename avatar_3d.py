import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class Avatar3D:
    def __init__(self):
        pygame.init()
        self.display = (800, 600)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Aria - Your AI Girlfriend")
        
        gluPerspective(45, (self.display[0]/self.display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)
        
        self.emotion = "neutral"
        self.blink_timer = 0
        self.breathing = 0
        
    def draw_sphere(self, radius, slices, stacks, color):
        glColor3f(*color)
        quad = gluNewQuadric()
        gluSphere(quad, radius, slices, stacks)
        
    def draw_face(self):
        # Head
        glPushMatrix()
        breathing_offset = np.sin(self.breathing) * 0.02
        glTranslatef(0, breathing_offset, 0)
        
        # Skin
        self.draw_sphere(1.0, 32, 32, (1.0, 0.85, 0.75))
        
        # Eyes
        glPushMatrix()
        glTranslatef(-0.3, 0.1, 0.85)
        if self.emotion == "happy":
            # Happy eyes (curved)
            glColor3f(0.2, 0.2, 0.2)
            self.draw_sphere(0.15, 16, 16, (0.2, 0.2, 0.2))
        else:
            self.draw_sphere(0.15, 16, 16, (1.0, 1.0, 1.0))
            glTranslatef(0, 0, 0.05)
            self.draw_sphere(0.08, 16, 16, (0.2, 0.4, 0.8))
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0.3, 0.1, 0.85)
        if self.emotion == "happy":
            self.draw_sphere(0.15, 16, 16, (0.2, 0.2, 0.2))
        else:
            self.draw_sphere(0.15, 16, 16, (1.0, 1.0, 1.0))
            glTranslatef(0, 0, 0.05)
            self.draw_sphere(0.08, 16, 16, (0.2, 0.4, 0.8))
        glPopMatrix()
        
        # Mouth
        glPushMatrix()
        glTranslatef(0, -0.3, 0.9)
        if self.emotion == "happy":
            # Smile
            glScalef(1.0, 0.3, 0.2)
            self.draw_sphere(0.3, 16, 16, (0.8, 0.4, 0.4))
        elif self.emotion == "sad":
            glScalef(1.0, 0.2, 0.2)
            glTranslatef(0, -0.1, 0)
            self.draw_sphere(0.3, 16, 16, (0.8, 0.4, 0.4))
        else:
            self.draw_sphere(0.2, 16, 16, (0.8, 0.4, 0.4))
        glPopMatrix()
        
        glPopMatrix()
        
    def set_emotion(self, emotion):
        self.emotion = emotion
        
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotatef(0.1, 0, 1, 0)
        
        self.breathing += 0.05
        
        self.draw_face()
        pygame.display.flip()
        pygame.time.wait(16)
        return True
    
    def cleanup(self):
        pygame.quit()

avatar = Avatar3D()