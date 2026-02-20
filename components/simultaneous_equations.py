from matrix import Matrix

class SimultaneousEquation:
    def __init__(self, a1, a2, b, c1, c2, d):
        """
        Creates a simultaneous equation of the form
        a1 * x + a2 * y = b
        c1 * x + c2 * y = d
        """
        self._matrix = None
        