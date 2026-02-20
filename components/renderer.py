import pygame
from components.particle import Particle
from components.vector import Vector
from components.constants import *

class Renderer:
    def __init__(self, win:pygame.Surface):
        self._zoom = 0
        self._offset = Vector(0, 0)
        
        self._win = win
        self._particles:list[Particle] = []

    def draw(self, vectors = False):
        for particle in self._particles:
            pygame.draw.circle(
                surface=self._win, color=BLACK,
                center=particle.get_location().to_tuple(),
                radius=particle.get_radius())
            
            if vectors:
                start = particle.get_location()
                pygame.draw.line(
                    surface=self._win, color=RED,
                    start_pos = start.to_tuple(),
                    end_pos = (start + particle.get_velocity()*10).to_tuple())


    