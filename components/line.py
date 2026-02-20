from components.vector import Vector


class Line:
    def __init__(self, a:Vector, b:Vector):
        self._a = a
        self._b = b
    
    def __str__(self):
        return self._a.__str__() + " to " + self._b.__str__()
        
    def y(self, x):
        if self._a.x <= x <= self._b.x or self._b.x <= x <= self._a.x:
            
            direction = self._b - self._a
            pos = self._a + direction * abs(x - self._a.x)/abs(self._a.x-self._b.x)
            return pos.y
        else:
            return -1
    
    def x(self, y):
        if self._a.y <= y <= self._b.y or self._b.y <= y <= self._a.y:
            
            direction = self._b - self._a
            pos = self._a + direction * abs(y - self._a.y)/abs(self._a.y-self._b.y)
            return pos.x
        else:
            return -1
    
    def check_collision(self, l:"Line"):
        # check for collinearity
        # check for where they would intersect
        
        
        #! check for vertical line: if so use x() instead
        
        # create a bounding strip containing 2 lines which span the strip
        # if they intersect, they must do so in this strip
        
        left = max(min(self._a.x, self._b.x), min(l._a.x, l._b.x))
        right = min(max(self._a.x, self._b.x), max(l._a.x, l._b.x))
        
        # check that one line is always above the other:
        # we round so that lines which are on top of each other will correctly set the difference to 0
        left1 = round(self.y(left), 5)
        right1 = round(self.y(right), 5)
        
        left2 = round(l.y(left), 5)
        right2 = round(l.y(right), 5)
                
        if (left1 - left2)*(right1 - right2) <= 0:
            return True
        else:
            return False