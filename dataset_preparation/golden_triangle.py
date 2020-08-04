# Function to calculate the value of n, being the original size of the protein & n x n dimensions of the original distance matrix
# I hope you like the name

class GoldenTriangle:

    def __init__(self):
        pass

    cache = {}
    def golden_triangle(n):   
        if n in cache:
            return cache[n]  
        if n == 4:
            value = 6
        elif n == 5:
            value = 10
        elif n == 6:
            value = 15
        elif n > 6:
            value = golden_triangle(n-1) + n - 1        
        cache[n] = value
        
        return value