from neuron import h
import numpy as np
import math
from scipy.signal import butter, lfilter
import sys
from stimStrat import biphasic

# count the number of spikes given a spike train
def firingRate(spikeTrain):
    threshold = -50
    aboveThresholdFlag = False
    aboveThresholdSpikes = []
    countSpike = 0
    for sp in spikeTrain:
        if sp > threshold:
            aboveThresholdFlag = True
            aboveThresholdSpikes.append(sp)
        else:
            if aboveThresholdFlag:
                if abs(max(aboveThresholdSpikes)-sp) > 40: 
                    countSpike = countSpike + 1
            aboveThresholdFlag = False
            aboveThresholdSpikes = []
    return countSpike

# load NEURON GUI
h.load_file("nrngui.hoc")

# specify the location of stimulating electrode (please adjust the 3D coordiante to suit your case)
e_3D = [5000, 400, -300]

# build nerve
h.load_file("nerve/sciaticNerveBuilder.hoc")  

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
nerve_R = 2100
nerve_L = 10100

substrate_3D = [5000, 0, 340]
substrate_W = 500
substrate_L = 4000
substrate_D = 30
e_R = 50            # change to 100, 200, 400 for the other three TIME diameters

fasc_3D = []
fasc_R = []
fasc_L = 10060
with open('../nerve/fasciclesInfo.txt', 'r') as f:
    for line in f.readlines():
        info = line.split(',')
        fasc_3D.append([float(info[0]),int(info[1]),int(info[2])])
        fasc_R.append(float(info[3]))

# optional arguments
rotate_deg = -45    # change to 0 and -90 for the other two insertion angles
simBox_G = 1.45
nerve_G = 0.01  
fasc_G = 0.0517
mesh_size = 3
e_type = "monopolar"
e2e_dist = None

# call the function to automate pipeline
tk.pipeline(path2server, path2mph, simBox_3D, simBox_size, nerve_3D, nerve_R, nerve_L, fasc_3D, fasc_R, fasc_L, \
                                substrate_3D, substrate_W, substrate_L, substrate_D, e_R, \
                                e_type=e_type, e2e_dist=e2e_dist, rotate_deg=rotate_deg, simBox_G=simBox_G, \
                                nerve_G=nerve_G, fasc_G=fasc_G, mesh_size=mesh_size)
"""

# set transfer resistances between the fibres and the electrode
h.load_file("setrx.hoc")

# attach electrode
h.load_file("attachStim.hoc")

# sort the fibres based on distance, store into array
dist = dict()
detected = []
Nsec = 0
for sec in h.allsec():
    Nsec = Nsec + 1

    # ignore section for electrode
    if str(sec) == 'sElec':
        continue

    # get fibre's ID
    secName = ''.join(e for e in str(sec) if e.isalnum())  # e.g. "AFibreBuilder11MYSA0"
    fibreType = secName[:6] # e.g. "AFibre"
    num = ""
    for c in secName[:17]:
        if c.isdigit():
            num = num + c
    fibreIndex = int(num)   # e.g. 11
    fibreName = fibreType + str(fibreIndex)

    # only process undetected fibres
    if fibreName in detected:
        continue
    detected.append(fibreName)

    # get fibre's distance to electrode
    dist[fibreName] = math.sqrt((sec.y3d(0)-e_3D[1])**2+(sec.z3d(0)-e_3D[2])**2)

fibres_od = sorted(dist, key=lambda fibre: (dist[fibre]))   # sort the dictionary by fibre's distance to electrode
print(fibres_od)

# loop through biphasic current
I = np.arange(0.01, 0.16, 0.01)
for amp in I:
    # assign stimulation waveform to electrode
    delay = 2                               # ms
    width = 0.1                             # ms
    gap = 0.05                              # ms
    last = 2                                # ms
    dt = 0.025                              # ms

    observeRange = 1170    # add an observation range, e.g. only observe the 10 closest fibres

    # attach electrode
    (h.stim_time, h.stim_amp) = biphasic(delay, amp, width, gap, last, dt)
    h.setstim()    # apply waveform to the electrode

    # detect fibres' responses
    """ fibre responses stored in the following dictionary (example):
    resp {
        "AFibre11": {
            "dist": 412.3,  
            "sr": 4
        }
        ...
    }
    """
    resp = dict()
    attDv = h.Vector()
    detected = []
    counter = 0
    for sec in h.allsec():
        # ignore section for electrode
        if str(sec) == 'sElec':
            continue

        # get fibre's ID
        secName = ''.join(e for e in str(sec) if e.isalnum())  # e.g. "AFibreBuilder11MYSA0"
        fibreType = secName[:6] # e.g. "AFibre"
        node = secName[-5:]
        num = ""
        for c in secName[:17]:
            if c.isdigit():
                num = num + c
        fibreIndex = int(num)   # e.g. 11
        fibreName = fibreType + str(fibreIndex)

        # ignore the first node for C fibre
        if fibreType == 'CFibre' and node == 'node0':
            continue

        # only process fibres within observation range
        if fibreName not in fibres_od[:observeRange]:
            continue

        # only process undetected fibres
        if fibreName in detected:
            continue
        detected.append(fibreName)

        # display progress
        counter = counter + 1
        sys.stdout.write("\r processing %f percent" % (counter/Nsec*100))
        sys.stdout.flush()

        resp[fibreName] = dict()

        # store 3D position info
        resp[fibreName]['y'] = sec.y3d(0)
        resp[fibreName]['z'] = sec.z3d(0)

        # detect fibre's spiking rate
        attDv.record(sec(0.5)._ref_v)
        if fibreType == "AFibre":
            h.v_init = -80
            h.dt = dt
            h.tstop = delay+2*width+gap+last
            h.run()
        else:
            h.v_init = -60
            h.dt = dt
            h.tstop = delay+2*width+gap+last
            h.run()

        spikeTrain = np.array(attDv)

        # remove stimulus artefacts by a filter
        b, a = butter(10, 3000, 'low', analog=False, fs=40000)
        spikeTrainFiltered = lfilter(b, a, spikeTrain+80)-80

        # store and plot response
        if fibreType == "AFibre":
            spikeRate = firingRate(spikeTrainFiltered)
            resp[fibreName]['sr'] = spikeRate
        else:
            spikeRate = firingRate(spikeTrainFiltered)
            resp[fibreName]['sr'] = spikeRate

    with open('data/biphasic/diam100_45degree_' + str(round(amp*1e3)) + 'uA.txt', 'w') as f:
        for fibre in fibres_od[:observeRange]:
            print('%s %g %g %g' % (fibre, resp[fibre]['y'], resp[fibre]['z'], resp[fibre]['sr']), file=f)