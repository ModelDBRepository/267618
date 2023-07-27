from neuron import h
import numpy as np
from stimStrat import KFS

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

# set transfer resistances between the fibre and the electrode
h.load_file("setrx.hoc")

# attach electrode
h.load_file("attachStim.hoc")

# assign stimulation waveform to electrode
delay = 10                              # ms
amps = np.arange(0.0005, 0.01, 0.0001)  # mA
freqs = np.arange(1e3, 10e3, 1e3)       # Hz, sinusoidal frequency in Hz
dur = 100                               # ms
last = 10                               # ms
dt = 0.005                              # ms

# detect fibres' responses
attDv = h.Vector()
for freq in freqs:
    for amp in amps:
        # attach electrode
        (h.stim_time, h.stim_amp) = KFS(delay, amp, freq, dur, last, dt)
        h.attach_stim()    # apply waveform to the electrode

        print('processing freq = %f kHz, amp = %f uA' % (freq/1e3, round(amp*1e3,2)))

        # detect fibre's spiking rate
        attDv.record(Afibre.node[0](0.5)._ref_v)
        h.v_init = -80
        h.dt = dt
        h.tstop = delay+dur+last
        h.run()

        spikeTrain = np.array(attDv)

        # write to file
        f = open("data/KFS/AFibre" + str(freq/1e3) + "kHz" + str(round(amp*1e3,2)) + "uA" + ".txt", "w")
        np.savetxt(f, spikeTrain)