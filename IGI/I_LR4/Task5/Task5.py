import numpy as np

class MatrixOperations:
    """
    Base class for matrix operations using NumPy.
    
    Attributes:
        matrix (numpy.ndarray): The matrix to perform operations on.
    """
    
    # Static attribute - class description
    description = "Matrix Operations Class"
    
    def __init__(self, n, m, low=1, high=100):
        """
        Initialize the matrix with random integers.
        
        Args:
            n (int): Number of rows.
            m (int): Number of columns.
            low (int): Minimum value for random numbers.
            high (int): Maximum value for random numbers.
        """
        self.matrix = np.random.randint(low, high, size=(n, m))
        print(f"Generated matrix:\n{self.matrix}")
    
    def row_sums(self):
        """Calculate sums of all rows."""
        return np.sum(self.matrix, axis=1)
    
    def min_row_sum(self):
        """Find the minimum value among row sums."""
        return np.min(self.row_sums())
    
    def even_odd_correlation(self):
        """
        Calculate correlation between elements with even and odd indices.
        
        Returns:
            float: Correlation coefficient.
        """
        # Flatten the matrix and separate even and odd indexed elements
        flat = self.matrix.flatten()
        even = flat[::2]  # Even indices
        odd = flat[1::2]  # Odd indices
        
        # Make sure both arrays have the same length
        min_len = min(len(even), len(odd))
        even = even[:min_len]
        odd = odd[:min_len]
        
        return np.corrcoef(even, odd)[0, 1]

class AdvancedMatrixOperations(MatrixOperations):
    """
    Extended matrix operations class with additional statistical methods.
    Inherits from MatrixOperations.
    """
    
    def __init__(self, n, m, low=1, high=100):
        """Initialize the advanced matrix operations."""
        super().__init__(n, m, low, high)
    
    def matrix_mean(self):
        """Calculate mean of all matrix elements."""
        return np.mean(self.matrix)
    
    def matrix_median(self):
        """Calculate median of all matrix elements."""
        return np.median(self.matrix)
    
    def matrix_variance(self):
        """Calculate variance of all matrix elements."""
        return np.var(self.matrix)
    
    def matrix_std_dev(self):
        """Calculate standard deviation of all matrix elements."""
        return np.std(self.matrix)

def main():
    """Main function to demonstrate the program functionality."""
    print("=== Matrix Operations Program ===")
    print("1. Basic Operations")
    print("2. Advanced Statistics")
    choice = input("Choose operation type (1/2): ")
    
    try:
        n = int(input("Enter number of rows: "))
        m = int(input("Enter number of columns: "))
    except ValueError:
        print("Please enter valid integers!")
        return
    
    if choice == '1':
        # Basic operations
        matrix = MatrixOperations(n, m)
        print("\nBasic Matrix Operations:")
        print(f"Row sums: {matrix.row_sums()}")
        print(f"Minimum row sum: {matrix.min_row_sum()}")
        print(f"Correlation between even/odd indexed elements: {matrix.even_odd_correlation():.4f}")
    
    elif choice == '2':
        # Advanced statistics
        matrix = AdvancedMatrixOperations(n, m)
        print("\nAdvanced Matrix Statistics:")
        print(f"Mean: {matrix.matrix_mean():.2f}")
        print(f"Median: {matrix.matrix_median()}")
        print(f"Variance: {matrix.matrix_variance():.2f}")
        print(f"Standard Deviation: {matrix.matrix_std_dev():.2f}")
        print(f"Minimum row sum: {matrix.min_row_sum()}")
        print(f"Correlation between even/odd indexed elements: {matrix.even_odd_correlation():.4f}")
    
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()