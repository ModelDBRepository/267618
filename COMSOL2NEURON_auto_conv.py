'''
This file is automatically run by the toolkit. Or, it can be seperately run by users. 

It imports and interpolates the .txt voltage profile from COMSOL to transfer resistance in NEURON.
'''

import pandas as pd
import numpy as np
from neuron import h
from scipy.interpolate import LinearNDInterpolator

def convert():
    # get 3D information about the points evaluated in COMSOL
    column_names = ['x', 'y', 'z', 'V']
    df = pd.read_csv('exStimVoltProf.txt', names=column_names, comment='%', delim_whitespace=True)
    x = np.array(df.x.to_list())
    y = np.array(df.y.to_list())
    z = np.array(df.z.to_list())
    points = np.array([x,y,z]).T
    V = np.array(df.V.to_list())
    
    # get the desired points to interpolate over in NEURON
    xi = np.array([])
    yi = np.array([])
    zi = np.array([])
    for sec in h.allsec():
        xi = np.append(xi, sec.x3d(0))
        yi = np.append(yi, sec.y3d(0))
        zi = np.append(zi, sec.z3d(0))

    # interpolate COMSOL's voltage profile according to NEURON's 3D geometry
    Vint = LinearNDInterpolator(points, V)

    # convert voltage profile into transfer resistance rx (unit: ohm)
    f = open("rx_xtra_interpolated.txt", "w")
    for sec in h.allsec():
        rx_xtra = Vint(np.array([sec.x3d(0), sec.y3d(0), sec.z3d(0)])) / 1e-6
        f.write("%f\n"%(rx_xtra))
    f.close()

    # assign the transfer resistance to each NEURON section
    h.load_file("setrx.hoc")