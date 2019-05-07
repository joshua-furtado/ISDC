import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

def dot_product(vector_one, vector_two):
        result = 0
        for i in range(len(vector_one)):
            result = result + vector_one[i]*vector_two[i]
        return result

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        
        if self.h == 1:
            det = self.g[0][0] # for 1x1 matrix
        else:
            det = self.g[0][0]*self.g[1][1] - self.g[0][1]*self.g[1][0] # for 2x2 matrix
        
        return det

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")
            
        trace = 0
        for i in range(self.h):
            trace = trace + self.g[i][i]
        
        return trace

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")

        if self.h == 1:
            inv = [[1/self.determinant()]] # for 1x1 matrix
        else:
            a = self.g[1][1]/self.determinant()
            b = -self.g[0][1]/self.determinant()
            c = -self.g[1][0]/self.determinant()
            d = self.g[0][0]/self.determinant()
            inv = [[a, b],[c, d]] # for 2x2 matrix
        
        return Matrix(inv)
        

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        trans = []
        
        for i in range(self.w):
            row = []
            for j in range(self.h):
                row.append(self.g[j][i])
            trans.append(row)
            
        return Matrix(trans)
        

    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
        
        matrixSum = []
        
        for i in range(self.h):
            row = []
            for j in range(self.w):
                row.append(self.g[i][j] + other.g[i][j])
            matrixSum.append(row)
            
        return Matrix(matrixSum)       

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        
        neg = []
        
        for i in range(self.h):
            row = []
            for j in range(self.w):
                row.append(-self.g[i][j])
            neg.append(row)
            
        return Matrix(neg)     


    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be subtracted if the dimensions are the same") 
        
        matrixDiff = []
        
        for i in range(self.h):
            row = []
            for j in range(self.w):
                row.append(self.g[i][j] - other.g[i][j])
            matrixDiff.append(row)
            
        return Matrix(matrixDiff)

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        
        if self.w != other.h:
            raise(ValueError, "Matrices cannot be multiplied") 
        
        product = []
        
        other_ = other.T() # transpose of other matrix
        
        for i in range(self.h):
            row = []
            for j in range(other.w):
                row.append(dot_product(self.g[i], other_[j]))
            product.append(row)
            
        return Matrix(product)

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            pass
            
        scaled = []
            
        for i in range(self.h):
            row = []
            for j in range(self.w):
                row.append(self.g[i][j]*other)
            scaled.append(row)
            
        return Matrix(scaled)