clc; clear;

Fs = 400000;
linewidth = 6;


%% SR for ramp amp
amp = [0:-0.0001:-0.0049];

onset = zeros([1 length(amp)]);
offset = zeros([1 length(amp)]);
for i = 1:length(amp)
    % read resp from files
    fileName = strcat('data/rampKFS/amp', sprintf("%.1f",amp(i)*1e3), 'uA_tdc50ms_tkfs200ms.txt');
    resp = readmatrix(fileName);

    % get firing rate
    onset_sr = firingRate(resp(1:30000));
    offset_sr = firingRate(resp(30000:end));
    onset(1,i) = onset_sr;
    offset(1,i) = offset_sr;
end

% plot onset & offset resp v.s. ramping amp
figure; hold on;
plot(amp, onset, 'Color', [0 0.4470 0.7410], 'linewidth', linewidth);
plot(amp, offset, 'Color', [0.6350 0.0780 0.1840], 'linewidth', linewidth);
xlabel('ramp amp (uA)');
ylabel('spike rate');
ylim([-0.5 5]);
hold off;


%% SR for ramp tao
fall = [0:10:300];

SR = zeros([1 length(fall)]);
for i = 1:length(fall)
    % read resp from files
    fileName = strcat('data/rampKFS/amp-3.0uA_tdc50ms_tkfs', sprintf("%d",fall(i)), 'ms.txt');
    resp = readmatrix(fileName);

    % get firing rate
    sr = firingRate(resp);
    SR(1,i) = sr;
end

% plot offset resp v.s. ramping time
figure; hold on;
plot(fall, SR, 'Color', [0.6350 0.0780 0.1840], 'linewidth', linewidth);
xlabel('ramp tao (ms)');
ylabel('spike rate');
ylim([-0.5 5]);
xlim([-50 300]);
hold off;


%% plot AP
amp = -0.003;   
fall = 200; 

% read resp from files
fileName = strcat('data/rampKFS/amp', sprintf("%.1f",amp*1e3), 'uA_tdc50ms_tkfs', sprintf("%d",fall), 'ms.txt');
resp = readmatrix(fileName);

% filter resp
[b, a] = butter(4, 1500/(Fs/2));
[h, w] = freqs(b, a);
respFiltered = filter(b, a, resp+80)-80;

figure; hold on;
plot(resp, 'linewidth', linewidth);
plot(respFiltered, 'linewidth', linewidth);
ylim([-100 40]);
hold off;


%% plot rampKFS waveform
figure; hold on;
delay = 10;
amp = -0.003;
platDur = 0;
sineDur = 0;
rise = 50;
sineAmp = 0.00245;
freq = 300;
fall = 240;
sineLast = 50;
dt = 0.005;
last = 10;

T = linspace(0,delay+rise+platDur+sineDur+fall+sineLast+last,1e4);
y = zeros([1 length(T)]);
for i = 1:length(T)
    if T(i) < delay
        y(i) = 0;	
    elseif T(i) < delay+rise
        y(i) = amp*(T(i)-delay)/rise;
    elseif T(i) < delay+rise+platDur
        y(i) = amp;      
    elseif T(i) < delay+rise+platDur+sineDur
        y(i) = amp + sineAmp * sin(2*pi*freq*(T(i)-delay-rise-platDur)/1000);
    elseif T(i) < delay+rise+platDur+sineDur+fall
        y(i) = amp - amp*(T(i) -delay-rise-platDur-sineDur)/fall + sineAmp * sin(2*pi*freq*(T(i)-delay-rise-platDur-sineDur)/1000);
    elseif T(i) < delay+rise+platDur+sineDur+fall+sineLast
        y(i) = sineAmp * sin(2*pi*freq*(T(i)-delay-rise-platDur-sineDur-fall)/1000);
    else
        y(i) = 0;
    end
end
plot(T, y, 'Color', [0 0.4470 0.7410], 'linewidth', linewidth);
xlabel('ramp time (ms)');
ylabel('amplitude (uA)');
hold off;