#Importing necessary libraries
import matplotlib.pyplot as plt
import random

# Facility class to represent the building space
class Facility:
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.grid = [[None for _ in range(width)] for _ in range(height)]

  def place_department(self, department, x, y):
    # Check if there's enough space for the department
    if x + department.width > self.width or y + department.height > self.height:
      return False

    # Check for overlaps with existing departments
    for i in range(department.width):
      for j in range(department.height):
        if self.grid[y+j][x+i] is not None:
          return False

    # Place the department on the grid
    for i in range(department.width):
      for j in range(department.height):
        self.grid[y+j][x+i] = department
    return True

# Department class to represent different functional areas
class Department:
  def __init__(self, name, width, height, adjacency_list=[]):
    self.name = name
    self.width = width
    self.height = height
    self.adjacency_list = adjacency_list  # List of departments it needs to be close to

# ALDEP function to generate a layout with visualization using Matplotlib
def ALDEP(facility, departments):
  # Shuffle the departments for random placement attempts
  random.shuffle(departments)

  # Try placing each department until successful
  for department in departments:
    placed = False
    # Depending on layout precision the number of attempts can be formulated
    for _ in range(100):  # Maximum of 100 attempts
      x = random.randint(0, facility.width - department.width)
      y = random.randint(0, facility.height - department.height)
      if facility.place_department(department, x, y):
        placed = True
        break

    if not placed:
      print(f"Failed to place department: {department.name}")

  # Create a color map for departments
  color_map = {'Department A': 'red', 'Department B': 'blue', 'Department C': 'green'}

  # Create the visualization using Matplotlib
  fig, ax = plt.subplots()

  # Set cell size based on facility dimensions
  cell_width = 1
  cell_height = 1

  # Iterate through the grid and create rectangles for departments
  for y in range(facility.height):
    for x in range(facility.width):
      department = facility.grid[y][x]
      if department:
        color = color_map.get(department.name, 'gray')  # Default gray for unknown departments
        rect = plt.Rectangle((x * cell_width, facility.height - (y + 1) * cell_height),
                             department.width * cell_width, department.height * cell_height, color=color)
        ax.add_patch(rect)

  # Set axis limits and labels (optional)
  ax.set_xlim(0, facility.width)
  ax.set_ylim(0, facility.height)
  ax.set_xlabel('X')
  ax.set_ylabel('Y')

  # Set title (optional)
  ax.set_title('Facility Layout')

  # Save or display the image
  plt.savefig('facility_layout.png')
  plt.show()

# Example usage
facility = Facility(200,50)
departments = [
  Department("Department A", 40, 15, ["Department B"]),
  Department("Department B", 8, 20),
  Department("Department C", 15, 20, ["Department A", "Department B"]),
  # Add more departments as needed
]

output = ALDEP(facility, departments)
print(output)



