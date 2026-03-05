import pygame
from components.particle import Particle
from components.vector import Vector
from components.constants import *
from math import exp

class Renderer:
    def __init__(self, win:pygame.Surface):
        """
        objects have coorindates which are then rendered onto a location on the screen
        
        the viewport has dimension WIDTH, HEIGHT when zoom is 1
        when zoom is 2, the viewport has dimension WIDTH/2, HEIGHT/2
        when zooming in, the offset is calculated as to keep the mouse at the same coordinates
        offset is written in terms of coordinates not location
        
        use zoom_controller to set an integer value for the scrolling then use a log
        transform to set the zoom level to appropriate value
        """
        
        
        self.__zoom_controller = 0
        self._zoom = 1
        self._zoom_sensitivity = 0.05
        self._offset = Vector(0, 0)
        
        self._win = win
    
    
    def _update_zoom(self):
        self._zoom = exp(self.__zoom_controller*self._zoom_sensitivity)
    
    
    def zoom(self, mouse_location:tuple[int, int], magnitude:int=1):
        
        # calculate the coordinates the mouse was pointing to
        mouse_location = Vector(*mouse_location)
        current_coords = (mouse_location - self._offset)/self._zoom
        
        # update the zoom
        self.__zoom_controller += magnitude
        self._update_zoom()
        
        # calculate the offset required to set the mouse to point at the same location
        self._offset = mouse_location - (current_coords * self._zoom)
        
        
    def offset(self, offset:tuple[int, int]):
        self._offset += Vector(offset[0], offset[1])


    def render(self, particles:list[Particle], draw_vectors = False, arrow_scale = 10):

        # draw the particles
        for particle in particles:
            
            centre_vector = (particle.get_location()*self._zoom + self._offset)
            radius = particle.get_radius()*self._zoom
            
            #* check that the particle is within the rendering distance
            if centre_vector + radius <= Vector(0, 0):
                pass

            elif centre_vector - radius >= Vector(WIDTH, HEIGHT):
                pass

            else:
                pygame.draw.circle(
                    surface=self._win, color=BLACK,
                    center=centre_vector.to_tuple(),
                    radius=radius)
                
                
                if draw_vectors:
                    end_pos = centre_vector + particle.get_velocity()*arrow_scale*self._zoom
                    pygame.draw.line(
                        surface=self._win, color=RED,
                        start_pos = centre_vector.to_tuple(),
                        end_pos = end_pos.to_tuple())
                    
        # draw scale markings
        
        
        


    