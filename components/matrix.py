import math
from decimal import Decimal

class Matrix:
    tolerance = 1e-10
    round_n_decimals = 10
    
    def __init__(self, dim:tuple[int, int]=(2, 2), values:list[float|int]=[]):
        """
        Recycles values to fill the matrix
        
        
        :param dim: the shape of the matrix
        :type dim: tuple[int, int]
        
        :param _values: the values of the matrix. if not specified, tries to fill using the identity
        :type _values: list[float|int]
        """
        self.dim = dim
        if not values:
            values = []
            for i in range(self.dim[1]):
                row = [0] * self.dim[1]
                row[i] = 1
                values.extend(row)
        
        n_rows = dim[0]
        n_cols = dim[1]
        self._matrix = [
            [
                values[(row*n_cols + col)%(len(values))] for col in range(n_cols)
            ] for row in range(n_rows)]
    
    
    @classmethod
    def from_2d_list(cls, matrix:list[list[float|int]]):
        dim = (len(matrix), len(matrix[0]))
        values = []
        for row in matrix:
            values.extend(row)
        
        return cls(dim=dim, values=values)
        
    
    def __str__(self):
        s = "["+"\n ".join([row.__str__() for row in self._matrix]) + "]"
        return s
    
    def __mul__(self, item:"Matrix|int|float"):
        if isinstance(item, Matrix):
            return self.matrix_multiplication(item)

        elif isinstance(item, float) or isinstance(item, int):
            return self.scalar_multiplication(item)
    
    def __rmul__(self, item:"Matrix|int|float"):
        if isinstance(item, Matrix):
            return item.matrix_multiplication(self)

        elif isinstance(item, float) or isinstance(item, int):
            return self.scalar_multiplication(item)
        
    def __getitem__(self, item):
        return self._matrix[item]
        
    def scalar_multiplication(self, scalar:int|float) -> "Matrix":
        values = []
        for row in self._matrix:
            values.extend([value * scalar for value in row])
        
        return Matrix(dim=self.dim, values=values)
    
    def matrix_multiplication(self, matrix:"Matrix"):
        """
        Multiplies this matrix by another matrix
        
        :param matrix: the matrix to multiply by
        :type matrix: "Matrix"
        """
        
        if self.dim[1] != matrix.dim[0]:
            raise ValueError(f"Cannot multiply matrix with shape ({self.dim[0]}, {self.dim[1]}) by matrix with shape ({matrix.dim[0]}, {matrix.dim[1]})")
        
        new_dim = (self.dim[0], matrix.dim[1])
        common_dim = self.dim[1]
        result = []
        for i in range(new_dim[0]):
            new_row = []
            for j in range(new_dim[1]):
                value = 0
                for k in range(common_dim):
                    value += self[i][k] * matrix[k][j]
                new_row.append(value)
            result.extend(new_row)
        
        return Matrix(dim=new_dim, values=result)
    
    def get_augmented_matrix(self):
        
        augmented_matrix = []
        for i, row in enumerate(self._matrix):
            aug_row = [0] * self.dim[0]
            aug_row[i] = 1
            augmented_matrix.append(row + aug_row)
        
        return Matrix.from_2d_list(augmented_matrix)
    
    @staticmethod
    def scale_row(row:list[float|int],
                  new_lead:float|int|None=None,
                  factor:float|int|None=None)->list[float|int]:
        """
        Scales the row.
        If new_lead is used, it scales by dividing by the leading non-zero and multiplying by new_lead
        If factor is used, it multiplies the row by that factor
        
        :param row: The list of numbers to scale
        :type row: list[float|int]
        :param new_lead: scales so that row's leading term is new_lead
        :type new_lead: float|int
        :param factor: multiplies by factor
        :type factor: float|int
        """
        if factor is None and new_lead is None:
            raise ValueError("Must scale row by factor or lead")
        
        if factor is not None and new_lead is not None:
            raise ValueError("Cannot scale row by factor and lead")
        
        if new_lead is not None:
            # find the first non-zero term
            first_term = Matrix.get_leading_term(row)
            
            scale = new_lead / (first_term)
        
        elif factor is not None:
            scale = factor
        
        return [x * scale for x in row]
        
    
    @staticmethod
    def get_leading_term(row:list[float]):
        first_term = 0
        for item in row:
            if item != 0:
                first_term = item
                break
            
        return first_term

    
    def rref(self) -> tuple["Matrix", dict[int, int]]:
        """
        Adapted from https://rosettacode.org/wiki/Reduced_row_echelon_form#Python
        """
        
        pivots = {}
        
        matrix = self._matrix[:]
        
        if not matrix:
            # empty matrix
            return Matrix.from_2d_list(matrix), pivots
        
        lead = 0
        row_count = len(matrix)
        column_count = len(matrix[0])
        for r in range(row_count):
            if lead >= column_count:
                # if the pivot column exceeds the matrix width
                return Matrix.from_2d_list(matrix), pivots
            i = r
            
            # finds the column with the next pivot is (lead)
            while matrix[i][lead] == 0:
                i += 1
                if i == row_count:
                    i = r
                    lead += 1
                    if column_count == lead:
                        # if there are no more pivots left
                        return Matrix.from_2d_list(matrix), pivots
            
            # swap the rows to move the pivot row to the correct location
            matrix[i],matrix[r] = matrix[r],matrix[i]
            
            # set the lead value to be 1
            lead_value = matrix[r][lead]
            matrix[r] = [ mrx / float(lead_value) for mrx in matrix[r]]
            
            pivots.update({lead:r})
            
            # reduce the other rows to 0 in the column containing the pivot
            for i in range(row_count):
                if i != r:
                    lead_value = matrix[i][lead]
                    matrix[i] = [ iv - lead_value*rv for rv,iv in zip(matrix[r],matrix[i])]
            lead += 1
        
        return Matrix.from_2d_list(matrix), pivots

    
    def invert(self):
        if self.dim[0] != self.dim[1]:
            raise RuntimeError("Cannot invert a non-square matrix")
        
        augmented_matrix = self.get_augmented_matrix()
        rref, _ = augmented_matrix.rref()
        inverse = []
        for row in rref:
            inverse.append(row[self.dim[0]:])
        return Matrix.from_2d_list(inverse)
    
    def round_matrix(self):
        matrix = self._matrix[:]
        for row in range(self.dim[0]):
            for col in range(self.dim[1]):
                matrix[row][col] = round(matrix[row][col], Matrix.round_n_decimals)
                v = Decimal(matrix[row][col])
                v = v.quantize(Decimal(Matrix.round_n_decimals))
                matrix[row][col] = float(v)
        return Matrix.from_2d_list(matrix)

if __name__ == "__main__":

    # M = Matrix(dim=(3, 3), values=[2, 1, 0, 1, 3, 1, 1, 2, 1])
    # M2 = Matrix(dim=(3, 3), values=[0, 2, 1, 2, 1, 0, 1, 3, 1])
    # I = Matrix(dim=(3, 3))

    # inv = M.invert()
    # print(inv)
    # inv.round_matrix()
    # print(inv)
    # print("="*60)
    # inv = M2.invert()
    # print(inv)
    # inv.round_matrix()
    # print(inv)

    # print(M2 * M)

    # M = Matrix.from_2d_list([[1, -3, 0, 5], [0, 0, 1, 7], [0, 0, 0, 0]])
    # M2 = Matrix.from_2d_list([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])

    # print(M)
    # print(M2)

    # print(M*M2)

    M = Matrix.from_2d_list([[1, -3, 0, 5], [0, 0, 1, 7], [0, 0, 0, 0]])
    # print(M.invert())
    M2 = Matrix.from_2d_list([[1, -3, 0, 5], [0, 0, 1, 7], [9, 2, 2, 1], [4, 3, 0, 0]])
    M2_inv = M2.invert()
    print(M2_inv.round_matrix())
    print((M2_inv * M2).round_matrix())
    M3 = Matrix.from_2d_list([[1, 2], [3, 4]])
    print(M3.invert())

