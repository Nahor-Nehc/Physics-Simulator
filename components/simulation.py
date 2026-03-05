from components.particle import Particle
from components.vector import Vector
from components.force import Force
from components.renderer import Renderer

import pygame


class Simulation:
    def __init__(self, win:pygame.Surface, gravity = 9.81):
        
        self._particles:list[Particle] = []
        
        self._renderer = Renderer(win=win)
        
        self._g = gravity
    
    def zoom(self, *args, **kwargs):
        self._renderer.zoom(*args, **kwargs)
    
    
    def offset(self, *args, **kwargs):
        self._renderer.offset(*args, **kwargs)
    
    
    def get_renderer(self):
        return self._renderer
    
    
    def render(self, vectors=True):
        self._renderer.render(particles=self._particles, draw_vectors=vectors)

    
    def update(self):
        for particle in self._particles:
            if self._g:
                particle.apply_force(Force(0, self._g))
            
            particle.update()
    
    
    def create_particle(self):
        pass

    