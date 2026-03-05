"""
A class which contains all the constants of a material which a particle can be made of
"""
from components.constants import *

class Material:
    def __init__(self):
        self._name = ""
        self._colour = BLACK # used to render the object
        self._charge = 0
        self._spring_constant = 0
        # self._youngs_modulus = 0
        

class Basic(Material):
    def __init__(self):
        super().__init__()
        self._name = "basic"
        self._colour = BLACK
        self._charge = 0
        self._spring_constant = 1