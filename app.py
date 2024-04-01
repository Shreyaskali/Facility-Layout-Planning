import streamlit as st
import pandas as pd

st.title("ALDEP")
st.write("This is a simple text. This will be description for the project")

st.header("Input for Facility Dimensions") # Part 1
st.write("Part 1: Input Facility width and height")

left_column, right_column = st.columns(2)
F_w = left_column.number_input("Insert a Facility Width", value=0, placeholder="Width...")
F_l = right_column.number_input("Insert a Facility Length", value=0, placeholder="Height...")
st.write('The facilty width is ', F_w)
st.write('The facility length is ', F_l)

st.header("Input number of departments") # Part 2
n = st.slider("N", 1, 10)
st.write('There are ', n, 'departments')

# st.write(*range(1, n+1))
st.header("Input for Department Dimensions") # Part 3
dept = []
data = []
for i in range(n):
    d = chr(i + ord('A'))
    dept.append(d)
    data.append([0, 0, []])

# option = st.selectbox('Select dept for input', dept)
# st.write(data)

for d in dept:
  option = d
  flag = 0
  left_column, mid, right_column = st.columns(3)
  left_column.write(f"Dimensions for Department {option}:")
  # st.write()
  idx = ord(option) - ord('A')
  L = left_column.slider('L')
  data[idx][0] = L
  W = left_column.slider('W')
  data[idx][1] = W

  with right_column:
      selected = st.multiselect('Select Adjacency list for department', dept)
      data[idx][2] = selected
      st.write('You selected:', selected)

  flag = st.button("Submit")
  if flag:
      st.write(data)
 
st.write(data)
st.header("Output") # Part 4
# -------------------------------------------------------------------------------------
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
        else:
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
    for _ in range(1000):  # Maximum of 100 attempts
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
  st.set_option('deprecation.showPyplotGlobalUse', False)
  output = plt.savefig('facility_layout.png')
  st.pyplot(output)
#   plt.show()

# Example usage
# facility = Facility(200,50)
departments = [
  Department("Department A", 40, 15, ["Department B"]),
  Department("Department B", 8, 20),
  Department("Department C", 15, 20, ["Department A", "Department B"]),
  # Add more departments as needed
]



facility = Facility(F_l, F_w)
# departments = [L, W, adj]

output = ALDEP(facility, departments)
print(output)


# -----------------------