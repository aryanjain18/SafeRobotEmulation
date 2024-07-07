    
    # These are the the real world coordinates of the points we will use to calculate the homography
ground_truth=[[0,0],       [109,0],          [218,0],
                    [54.5,55.2],     [163.5,55.2],
                  [0,110.4],    [109,110.4],      [218,110.4],
                    [54.5, 165.6], [163.5, 165.6],
                  [0.0, 220.8], [109.0, 220.8],   [218.0, 220.8]]
    
def is_within_boundaries(matrix, coordinates):
    
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0

    x, y = coordinates

    if 0 <= x < rows and 0 <= y < cols:
        return True
    else:
        return False

# Example usage:
matrix = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

# Coordinates to check
coordinates = (2, 3)

# Check if the coordinates are within the boundaries
result = is_within_boundaries(matrix, coordinates)

if result:
    print(f"The coordinates {coordinates} are within the boundaries of the matrix.")
else:
    print(f"The coordinates {coordinates} are outside the boundaries of the matrix.")

