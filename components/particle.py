from components.vector import Vector
from components.line import Line
from components.force import Force

class Particle:
    def __init__(self, radius:float|int, mass:float|int, location:Vector, time_delta:float):
        self._radius = radius
        self._mass = mass
        self._location = location
        self._previous_location = location
        self._time_delta = time_delta # this is the time between frames
        self._velocity = Vector(0, 0)
        self._forces:list[Force] = []
    
    def get_velocity(self):
        return self._velocity
    
    def get_location(self) -> Vector:
        return self._location
    
    def get_radius(self) -> float|int:
        return self._radius
    
    def get_particle_shadow(self):
        displacement = self._previous_location.to(self._location)
        perpendicular_radius = displacement.get_perp().get_unit() * self._radius

        l1_a = self._previous_location + perpendicular_radius
        l1_b = self._previous_location + displacement + perpendicular_radius
        l2_a = self._previous_location - perpendicular_radius
        l2_b = self._previous_location + displacement - perpendicular_radius
        
        l1 = Line(l1_a, l1_b)
        l2 = Line(l2_a, l2_b)
        
        return l1, l2
    
    def _check_collision_occured(self, particle:"Particle"):
        # we want to draw a line from the initial locations of the particles
        # to their current location and see if they touched at any point
        
        # create the two lines which mark where the particle has travelled
        # in the last frame (the shadow). Find if any of the lines overlap.
        
        # this particle's displacement
        l1, l2 = self.get_particle_shadow()
        
        print(l1, l2)
        
        # target particle's displacement
        l3, l4 = particle.get_particle_shadow()
        
        print(l3, l4)
        
        for line1 in [l1, l2]:
            for line2 in [l3, l4]:
                if line2.check_collision(line1):
                    return True
        
        return False
        
        
    def collide(self, particle:"Particle"):
        pass
    
    def apply_force(self, force:Force):
        self._forces.append(force)
    

    def update(self):
        resultant_force = Force(0, 0)
        
        for force in self._forces:
            resultant_force += force

        # F = ma
        accel = resultant_force / self._mass

        # a = v/t
        delta_v = accel * self._time_delta
        
        self._velocity += delta_v
        
        self._previous_location = self._location
        
        self._location += self._velocity
        
        self._forces = []
        

if __name__ == "__main__":
    p1 = Particle(5, 10, Vector(50, 70), 0.1)
    p1._previous_location = Vector(90, 70)
    p2 = Particle(5, 10, Vector(70, 50), 0.1)
    p2._previous_location = Vector(70, 90)

    print(p1._check_collision_occured(p2))