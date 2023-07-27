from math import sin, pi
from neuron import h

'''
Waveform for kilohertz stimulation
Input:
delay:      delay of KFS
amp:        amplitude of KFS
freq:       frequency of KFS
dur:        duration of KFS
last:       duration of silence
dt:         time resolution
'''
def KFS(delay, amp, freq, dur, last, dt):
    N = int((delay+dur+last) / dt) + 1  # +1 in length to avoid vm hyp issue
    h.stim_amp.resize(N)  
    h.stim_amp.fill(0)
    h.stim_time.resize(N)
    h.stim_time.fill(0)

    # stim time
    for i in range(0, N):
        h.stim_time[i] = i*(delay+dur+last) / N

    # stim values
    for i in range(0, N):
        if h.stim_time[i] < delay:
            h.stim_amp[i] = 0	
        elif h.stim_time[i] < delay+dur:
            h.stim_amp[i] = amp*sin(2*pi*freq*(h.stim_time[i]-delay-dur)/1000)
        else:
            h.stim_amp[i] = 0

    return (h.stim_time, h.stim_amp)

'''
Waveform for cathodic ramp combined with kilohertz stimulation
Input:
delay:      delay of waveform
amp:        ramp amplitude of cathodic ramp
rise:       ramp time of cathodic ramp
platDur:    duration of cathodic ramp plateau
sineAmp:    amplitude of KFS
freq:       frequency of KFS
sineDur:    duration of anodic KFS
fall:       ramp time of anodic KFS ramp
sineLast:   duration of KFS at zero DC offset
last:       duration of silence
dt:         time resolution
'''
def rampKFS(delay, amp, rise, platDur, sineAmp, freq, sineDur, fall, sineLast, last, dt):
    N = int((delay+rise+platDur+sineDur+fall+sineLast+last) / dt) + 1  # +1 in length to avoid vm hyp issue
    h.stim_amp.resize(N)  
    h.stim_amp.fill(0)
    h.stim_time.resize(N)
    h.stim_time.fill(0)

    # stim time
    for i in range(0, N):
        h.stim_time[i] = i*(delay+rise+platDur+sineDur+fall+sineLast+last) / N

    # stim values
    for i in range(0, N):
        if h.stim_time[i] < delay:
            h.stim_amp[i] = 0	
        elif h.stim_time[i] < delay+rise:
            h.stim_amp[i] = amp*(h.stim_time[i]-delay)/rise
        elif h.stim_time[i] < delay+rise+platDur:
            h.stim_amp[i] = amp      
        elif h.stim_time[i] < delay+rise+platDur+sineDur:
            h.stim_amp[i] = amp + sineAmp * sin(2*pi*freq*(h.stim_time[i]-delay-rise-platDur)/1000)
        elif h.stim_time[i] < delay+rise+platDur+sineDur+fall:
            h.stim_amp[i] = amp - amp*(h.stim_time[i]-delay-rise-platDur-sineDur)/fall + sineAmp * sin(2*pi*freq*(h.stim_time[i]-delay-rise-platDur-sineDur)/1000)
        elif h.stim_time[i] < delay+rise+platDur+sineDur+fall+sineLast:
            h.stim_amp[i] = sineAmp * sin(2*pi*freq*(h.stim_time[i]-delay-rise-platDur-sineDur-fall)/1000)
        else:
            h.stim_amp[i] = 0

    return (h.stim_time, h.stim_amp)

'''
Waveform for biphasic stimulation
Input:
delay:      delay of biphasic waveform
amp:        amplitude of biphasic waveform
width:      pulse width of biphasic waveform
gap:        gap (interval) between biphasic pulses
last:       duration of silence
dt:         time resolution
'''
def biphasic(delay, amp, width, gap, last, dt):
    N = int((delay+2*width+gap+last) / dt) + 1  # +1 in length to avoid vm hyp issue
    h.stim_amp.resize(N)  
    h.stim_amp.fill(0)
    h.stim_time.resize(N)
    h.stim_time.fill(0)

    # stim time
    for i in range(0, N):
        h.stim_time[i] = i*(delay+2*width+gap+last) / N

    # stim values
    for i in range(0, N):
        if h.stim_time[i] < delay:
            h.stim_amp[i] = 0	
        elif h.stim_time[i] < delay+width:
            h.stim_amp[i] = -1*amp
        elif h.stim_time[i] < delay+width+gap:
            h.stim_amp[i] = 0
        elif h.stim_time[i] < delay+2*width+gap:
            h.stim_amp[i] = amp
        else:
            h.stim_amp[i] = 0

    return (h.stim_time, h.stim_amp)