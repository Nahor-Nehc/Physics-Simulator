from components.particle import Particle
from components.vector import Vector
from components.force import Force
from components.renderer import Renderer
from components.simulation import Simulation
from components.constants import *

import pygame
pygame.init()

def handle_events(events, sim:Simulation):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            
            import sys
            sys.exit()
        
        if event.type == pygame.MOUSEWHEEL:
            sim.zoom(mouse_location=pygame.mouse.get_pos(),
                     magnitude=event.y)
        
        elif event.type == pygame.MOUSEMOTION:
            
            # print(pygame.mouse.get_pressed)
            if pygame.mouse.get_pressed()[0]:
                sim.offset(event.rel)
                
            


def main():
    # display window that is drawn to
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Physics Simulator")

    clock = pygame.time.Clock()
    
    sim = Simulation(win=win)
    p1 = Particle(50, 4, Vector(100, 500), 1/FPS)
    p1._velocity = Vector(2, -5)
    p2 = Particle(100, 4, Vector(800, 200), 1/FPS)
    sim._particles = [p1, p2]

    run = True
    while run:
        
        # print(pygame.display.get_current_refresh_rate())
        clock.tick(FPS)

        events = pygame.event.get()
        handle_events(events, sim)
        
        sim.update()
        win.fill(WHITE)
        sim.render()
        pygame.display.update()
        
if __name__ == "__main__":
    main()
