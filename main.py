from components.particle import Particle
from components.vector import Vector
from components.force import Force
from components.renderer import Renderer
from components.constants import *

import pygame
pygame.init()

def handle_events(events):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            
            import sys
            sys.exit()


def main():
    # display window that is drawn to
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("insert")

    clock = pygame.time.Clock()
    
    renderer = Renderer(win)
    p1 = Particle(50, 4, Vector(100, 500), 1/FPS)
    p1._velocity = Vector(2, -5)
    p2 = Particle(100, 4, Vector(800, 200), 1/FPS)
    renderer._particles = [p1, p2]

    run = True
    while run:
        clock.tick(FPS)

        events = pygame.event.get()
        handle_events(events)
        
        p1.apply_force(Force(0, 9.8))
        
        p1.update()
        p2.update()
        
        win.fill(WHITE)
        renderer.draw(vectors=True)
        pygame.display.update()
        
if __name__ == "__main__":
    main()
