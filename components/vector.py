class Vector:
    """
    A two dimensional vector with components stored as x and y
    """
    tolerance = 1e-10 # -13 for is_collinear
    
    
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __add__(self, item):
        return self.add(item)
    
    def __abs__(self):
        return (self.x**2 + self.y**2)**0.5
    
    def __radd__(self, item):
        return self.add(item)
    
    def __sub__(self, item):
        return self.subtract(item)
        
    def __rsub__(self, item):
        return self.rsubtract(item)
    
    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __mul__(self, item):
        if isinstance(item, Vector):
            return self.dot(item)
        
        if isinstance(item, int) or isinstance(item, float):
            return self.mul(item)
        
        else:
            raise ValueError(f"Must multiply type 'Vector' or 'int' or 'float', not {type(item)}")
    
    def __rmul__(self, item):
        return self * item
    
    def __bool__(self):
        return (self.x != 0) or (self.y != 0)
    
    def __truediv__(self, item):
        if item == 0:
            raise ZeroDivisionError("Cannot divide a vector by 0")
        if isinstance(item, int) or isinstance(item, float):
            return self.mul(1/item)
        else:
            raise ValueError(f"Must divide by type 'int' or 'float', not {type(item)}")
    
    def to_tuple(self):
        return (self.x, self.y)
    
    def dot(self, v) -> int|float:
        return self.x * v.x + self.y * v.y
    
    def add(self, item) -> "Vector":
        if isinstance(item, Vector):
            return Vector(self.x + item.x, self.y + item.y)
        elif isinstance(item, int) or isinstance(item, float):
            return Vector(self.x + item, self.y + item)
        else:
            raise ValueError(f"Must add type 'Vector' or 'int' or 'float', not {type(item)}")
    
    def subtract(self, item) -> "Vector":
        """
        Subtract a vector or scalar from this vector
        
        :param self: Description
        :param item: Description
        :type item: Vector|float|int
        """
        if isinstance(item, Vector):
            return Vector(self.x - item.x, self.y - item.y)
        elif isinstance(item, int) or isinstance(item, float):
            return Vector(self.x - item, self.y - item)
        else:
            raise ValueError(f"Must subtract type 'Vector' or 'int' or 'float', not {type(item)}")
    
    def rsubtract(self, item):
        if isinstance(item, Vector):
            return Vector(item.x - self.x, item.y - self.y)
        elif isinstance(item, int) or isinstance(item, float):
            return Vector(item - self.x, item - self.y)
        else:
            raise ValueError(f"Must add type 'Vector' or 'int' or 'float', not {type(item)}")

    def mul(self, scalar:int|float):
        return Vector(self.x * scalar, self.y * scalar)

    def get_perp(self):
        """
        returns a Vector which is perpendicular to itself
        """
        return Vector(-1 * self.y, self.x)
    
    def get_unit(self):
        return Vector(self.x, self.y)/abs(self)
    
    def to(self, v:"Vector"):
        return v.subtract(self)
    
    def is_collinear(self, v:"Vector"):
        if self and v:
            value = abs(self.dot(v) / (abs(self)*abs(v)))
            print(value)
            if abs(value - 1) < Vector.tolerance:
                return True
            return False
        
        return True


if __name__ == "__main__":
    v1 = Vector(1, 1)
    v2 = Vector(2, 1)
    v3 = Vector(2, 2)
    v4 = Vector(-2, -2)

    print(v1.is_collinear(v2))
    print(v1.is_collinear(v3))
    print(v1.is_collinear(v4))

