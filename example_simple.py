'''
toolkit example for a simple nerve containing one fascicle and two fibres
'''

# Step 1: import headers for (i) NEURON's .hoc object and (ii) autoToolkit
from neuron import h
import autoToolkit as tk

# Step 2: build your own NEURON model (e.g., create a simple fascicle in NEURON)
h.load_file(r"nerve/simpleFascicle.hoc")

# Step 3: define arguements
path2server = 'C:\\Program Files\\COMSOL\\COMSOL56\\Multiphysics\\bin\\win64'
path2mph = 'C:\\Program Files\\COMSOL\\COMSOL56\\Multiphysics\\mli'

simBox_3D = [500, 0, 0]
simBox_size = 1200

nerve_3D = [-50, 0, 0]
nerve_R = 400
nerve_L = 1100

substrate_3D = [500, 0, -250]
substrate_W = 200
substrate_L = 1000
substrate_D = 30
e_R = 10

fasc_3D = [[-3, 0, 0]]
fasc_R = [200]
fasc_L = 1006

# Step 4: call the function to automate pipeline
tk.pipeline(path2server, path2mph, simBox_3D, simBox_size, nerve_3D, nerve_R, nerve_L, fasc_3D, fasc_R, fasc_L, \
                                substrate_3D, substrate_W, substrate_L, substrate_D, e_R)