from neuron import h
import numpy as np
from stimStrat import rampKFS

# load NEURON GUI
h.load_file("nrngui.hoc")

# build fibres
h.load_file("nerve/AFibreBuilder.hoc")  
Afibre = h.AFibreBuilder(0,0,0) 

""" 
# Uncommment to automatically run the toolkit if you don't have the rx_xtra_interpolated.txt already in the directory.

# import toolkit header
import autoToolkit as tk

# define arguments
path2server = 'C:\\Program Files\\COMSOL\\COMSOL56\\Multiphysics\\bin\\win64'
path2mph = 'C:\\Program Files\\COMSOL\\COMSOL56\\Multiphysics\\mli'

simBox_3D = [5000, 0, 0]
simBox_size = 12000

nerve_3D = [-50, 0, 0]
nerve_R = 400
nerve_L = 10100

substrate_3D = [5000, 0, -216]
substrate_W = 500
substrate_L = 4000
substrate_D = 30
e_R = 10

fasc_3D = [[-30, 0, 0]]
fasc_R = [200]
fasc_L = 10060

# call the function to automate pipeline
tk.pipeline(path2server, path2mph, simBox_3D, simBox_size, nerve_3D, nerve_R, nerve_L, fasc_3D, fasc_R, fasc_L, \
                                substrate_3D, substrate_W, substrate_L, substrate_D, e_R)
"""

# set transfer resistances between the fibres and the electrode
h.load_file("setrx.hoc")

# attach electrode
h.load_file("attachStim.hoc")

# assign stimulation waveform to electrode
delay = 10                          # ms
amps = np.arange(0,-0.005,-0.0001)  # mA, cathodic DC ramp amplitude
rise = 50                           # ms, cathodic DC ramp time
platDur = 0                         # ms
sineDur = 0                         # ms
sineAmp = 0.00245                   # mA, KFS amplitude
freq = 3e3                          # Hz
fall = 200                          # ms, anodic KFS ramp time
sineLast = 50                       # ms
dt = 0.005                          # ms
last = 10                           # ms

# ramp amp
attDv = h.Vector()
for amp in amps:
    # attach electrode
    (h.stim_time, h.stim_amp) = rampKFS(delay, amp, rise, platDur, sineAmp, freq, sineDur, fall, sineLast, last, dt)
    h.attach_stim()    # apply waveform to the electrode

    # detect fibre's spiking rate
    attDv.record(Afibre.node[0](0.5)._ref_v)
    h.v_init = -80
    h.dt = dt
    h.tstop = delay+rise+platDur+sineDur+fall+sineLast+last
    h.run()

    spikeTrain = np.array(attDv)

    # write to file
    f = open("data/rampKFS/amp" + str(round(amp*1e3,2)) + "uA_tdc50ms_" + "tkfs200ms.txt", "w")
    np.savetxt(f, spikeTrain)