'''
A toolkit example for a complex sciatic nerve as mentioned in the manuscript
'''

# Step 1: import headers for (i) NEURON's .hoc object and (ii) autoToolkit
from neuron import h
import autoToolkit as tk

# Step 2: build your own NEURON model (e.g., create sciatic nerve in NEURON)
h.load_file(r"nerve/sciaticNerveBuilder.hoc")

# Step 3: define arguements
path2server = 'C:\\Program Files\\COMSOL\\COMSOL56\\Multiphysics\\bin\\win64'
path2mph = 'C:\\Program Files\\COMSOL\\COMSOL56\\Multiphysics\\mli'

simBox_3D = [5000, 0, 0]
simBox_size = 12000

nerve_3D = [-50, 0, 0]
nerve_R = 2100
nerve_L = 10100

substrate_3D = [5000, 0, 340]
substrate_W = 500
substrate_L = 4000
substrate_D = 30
e_R = 10

fasc_3D = []
fasc_R = []
fasc_L = 10060
with open('nerve/fasciclesInfo.txt', 'r') as f:
    for line in f.readlines():
        info = line.split(',')
        fasc_3D.append([float(info[0]),int(info[1]),int(info[2])])
        fasc_R.append(float(info[3]))

# optional arguements
rotate_deg = -50
simBox_G = 1.45
nerve_G = 0.01  
fasc_G = 0.0517
mesh_size = 3
e_type = "monopolar"
e2e_dist = 80

# Step 4: call the function to automate pipeline
tk.pipeline(path2server, path2mph, simBox_3D, simBox_size, nerve_3D, nerve_R, nerve_L, fasc_3D, fasc_R, fasc_L, \
                                substrate_3D, substrate_W, substrate_L, substrate_D, e_R, \
                                e_type=e_type, e2e_dist=e2e_dist, rotate_deg=rotate_deg, simBox_G=simBox_G, \
                                nerve_G=nerve_G, fasc_G=fasc_G, mesh_size=mesh_size)