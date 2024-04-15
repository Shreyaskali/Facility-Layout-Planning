import streamlit as st
import matplotlib.pyplot as plt
import random
import numpy as np
import uuid

st.set_page_config(page_title="ALDEP")
st.title("ALDEP")

st.write("This is a simple text. This will be description for the project")

st.header("Input for Facility Dimensions") # Part 1

left, right = st.columns(2)
F_w = left.number_input("Insert a Facility Width", value=0, placeholder="Width...")
F_l = right.number_input("Insert a Facility Length", value=0, placeholder="Height...")


st.header("Input number of departments")
n = st.slider("N", 1, 10)
st.write('There are ', n, 'departments')

st.header("Input for Department Dimensions")
dept = []
data = []
for i in range(n):
    d = chr(i + ord('A'))
    dept.append(d)
    data.append([0, 0, []])

def checkArea(l,b,data):
  area = 0
  for i in range(n):
    area += data[i][0]*data[i][1]
  if(area>l*b):
    st.warning("Insufficient Facility Dimensions!")
    return 0
  else:
    return 1

val = 1
flag = 0
for d in dept:
  
  very_left,left, mid, right = st.columns(4)
  very_left.write(f"Department {d}:")
  
  idx = ord(d) - ord("A")

  L = left.number_input('L',value=0,key=val)

  data[idx][0] = L
  W = mid.number_input('W',value=0,key=val+1)
  
  data[idx][1] = W

  with right:
      selected = st.multiselect('Adjacency list', dept, key=val+2)
      data[idx][2] = selected
  val+=3
ans = st.button("Submit")
if ans:
    # st.write(data)
    flag = checkArea(F_l, F_w, data)
  
st.header("Output") 
# -------------------------------------------------------------------------------------
# Facility class to represent the building space
class Facility:
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.grid = [[None for _ in range(width)] for _ in range(height)]

# Department class to represent different functional areas
class Department:
  def __init__(self, name, width, height, adjacency_list=[]):
    self.name = name
    self.width = width
    self.height = height
    self.adjacency_list = adjacency_list  # List of departments it needs to be close to

# ALDEP function to generate a layout with visualization using Matplotlib
def ALDEP(facility, data):
  initdept = random.randint(0, n-1)
  prev = -1
  deptlist = []
  visited = [0 for i in range(n)]
  deptlist.append(initdept)
  visited[initdept] = 1
  curr = initdept

  while deptlist[-1] != prev:
      prev = deptlist[-1]
      adjacencylist = data[prev][2]

      for i in range(len(adjacencylist)):
          if not visited[i]:
              visited[i] = 1
              deptlist.append(i)
              break

  for i in range(n):
      if not visited[i]:
          deptlist.append(i)
          visited[i] = 1
          prev = -1

          while deptlist[-1] != prev:
              prev = deptlist[-1]
              adjacencylist = data[prev][2]

              for i in range(len(adjacencylist)):
                  if not visited[i]:
                      visited[i] = 1
                      deptlist.append(i)
                      break
  print(deptlist) 

  areas = []
  block = F_w
  for dept in data:
    areas.append(dept[0] * dept[1])
    block = min(dept[0], block)
    block = min(dept[1], block)

  print(areas)
  sweepwidth = 1
  print(block)
  

  # F_w = 100
  # F_l = 100
  L = int(F_l / block)
  W = int(F_w / block)
  facility = [[0 for i in range(L)] for j in range(W)]
  facility = np.array(facility)

  start_w, start_l = 0, 0

  for dept in deptlist:
    # print("dept", dept)
    # print("start:", start_w, start_l)
    deptarea = areas[dept]

    direction = start_l % 2

    if not direction:
      partial1 = (W - start_w)
    else:
      partial1 = start_w

    deptarea -= partial1 * block
    full = (deptarea // block) // W
    partial = (deptarea // block) % W

    # print(deptarea, partial1, full, partial)

    if partial1 != 0:
      if not direction:
        for i in range(partial1):
            facility[start_w + i, start_l] = dept + 1
      else:
        for i in range(partial1-1, -1, -1):
          facility[i, start_l] = dept + 1

      # print(facility, "printed partial1\n")
      start_l += 1

    # print(full, partial)

    for j in range(full):
      facility[:, start_l + j] = dept + 1
      # print(facility, "printed full\n")

    start_l += full
    # print(full, partial)

    if start_l % 2 == 0:
      for i in range(partial):
        facility[i, start_l] = dept + 1
      start_w += partial
    elif partial != 0:
      for i in range(W-1, W-partial-1, -1):
        facility[i, start_l] = dept + 1
      # print(facility, "printed partial\n")
      start_w += W-partial


    start_w += partial1
    start_w %= W
  
  print(facility)
  # print(start_w, start_l)
  
  # # Create a color map for departments
  # color_map = {'A': '#03071e', 'B': '#370617', 'C': '#6a040f','D':'#9d0208','E':'#d00000','F':'#dc2f02','G':'#e85d04','H':'#f48c06','I':'#faa307','J':'#ffba08'}

  # # Create the visualization using Matplotlib
  # fig, ax = plt.subplots()

  # # Set cell size based on facility dimensions
  # cell_width = 1
  # cell_height = 1

  # # Iterate through the grid and create rectangles for departments
  # for x in range(facility.height):
  #   for y in range(facility.width):
  #     department = facility.grid[x][y]
  #     if department:
  #       color = color_map.get(department.name, 'gray')  # Default gray for unknown departments
  #       rect = plt.Rectangle((y * cell_width, facility.height - (x + 1) * cell_height),
  #                            department.width * cell_width, department.height * cell_height, color=color)
  #       ax.add_patch(rect)

  # # Set axis limits and labels (optional)
  # ax.set_xlim(0, facility.width)
  # ax.set_ylim(0, facility.height)
  # ax.set_xlabel('X')
  # ax.set_ylabel('Y')

  # # Set title (optional)
  # ax.set_title('Facility Layout')
  # Importing required modules
  plt.rcParams['figure.figsize']=(7,5)


  plt.gca().invert_yaxis()
  # Generating colormesh using pcolormesh() funcion
  plt.pcolormesh(facility,cmap='GnBu')
    
  # Adding details to the plot    
  plt.title('Facility Layout')
  plt.xlabel('x-axis')
  plt.ylabel('y-axis')
  plt.legend()
  # Displaying the plot
  plt.show()

  # Save or display the image
  st.set_option('deprecation.showPyplotGlobalUse', False)
  output = plt.savefig('facility_layout.png')
  st.pyplot(output)
#   plt.show()

# Example usage
# facility = Facility(200,50)
# departments = [
#   Department("A", 40, 15, ["B"]),
#   Department("B", 8, 20),
#   Department("C", 15, 20, ["A", "B"]),
#   # Add more departments as needed
# ]


# Dynamic addition of departments
departments =[]
if flag:
  for i in range(int(n)):
    departments.append(Department(dept[i],int(data[i][0]),int(data[i][1]),data[i][2]))

print(departments)


facility = Facility(F_l, F_w)
# departments = [L, W, adj]

try:
  output = ALDEP(facility, data)
  print(output)
except ValueError:
  st.warning("Insufficient Facility Dimensions")
