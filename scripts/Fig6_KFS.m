clc; clear;

linewidth = 10;
Fs = 400000;


%% color map for A fibre

amplitudes = [0.5:0.1:9.9];
frequencies = [1:0.1:9.9]*1e3;

C = zeros([length(frequencies) length(amplitudes)]);

for i = 1:length(amplitudes)
    for j = 1:length(frequencies)
        % read from resp
        fileName = strcat('data/KFS/AFibre', sprintf("%.1f",frequencies(j)/1e3), 'kHz', sprintf("%.1f",amplitudes(i)), 'uA.txt');
        resp = readmatrix(fileName);

        % get firing rate
        sr = firingRate(resp);

        % store in colormap
        C(j,i) = sr;
    end
end

% plot colormap
imagesc(amplitudes, frequencies, C);
set(gca,'YDir','normal');
colorbar;
xlabel('amplitude (uA)');
ylabel('frequency (kHz)');


%% spike rate plot for A fibre

frequency = 4e3;
amplitudesA = [0.5:0.1:9.9];  % uA
SRA = [];
for i = 1:length(amplitudesA)
    % read from resp
    fileNameA = strcat('data/KFS/AFibre', sprintf("%.1f",frequency/1e3), 'kHz', sprintf("%.1f",amplitudesA(i)), 'uA.txt');
    respA = readmatrix(fileNameA);

    % get firing rate
    srA = firingRate(respA);
    SRA = [SRA, srA];
end

figure; hold on;
plot(amplitudesA, SRA, 'linewidth', linewidth);
xlabel('amplitude (uA)');
ylabel('SR');
ylim([-10 30]);


%% AP plot for A fibre
frequency = 4e3;
amplitude = 3;

% read from resp
fileNameA = strcat('data/KFS/AFibre', sprintf("%.1f",frequency/1e3), 'kHz', sprintf("%.1f",amplitude), 'uA.txt');
respA = readmatrix(fileNameA);

figure; hold on;
plot(respA, 'linewidth', linewidth);
xlabel('amplitude (uA)');
ylabel('NSR');
ylim([-100 50]);


%% color map for C fibre

amplitudes = [10:10:990];
frequencies = [1:0.1:9.9]*1e3;

C = zeros([length(frequencies) length(amplitudes)]);

for i = 1:length(amplitudes)
    for j = 1:length(frequencies)
        % read from resp
        fileName = strcat('data/KFS/CFibre', sprintf("%.1f",frequencies(j)/1e3), 'kHz', sprintf("%.1f",amplitudes(i)), 'uA.txt');
        resp = readmatrix(fileName);

        % get firing rate
        sr = firingRate(resp);

        % store in colormap
        C(j,i) = sr;
    end
end

% plot colormap
figure;
imagesc(amplitudes, frequencies, C);
set(gca,'YDir','normal');
colorbar;
xlabel('amplitude (uA)');
ylabel('frequency (kHz)');


%% spike rate plot for C fibre
frequency = 4e3;
amplitudesC = [10:10:990];  % uA
SRC = [];
for i = 1:length(amplitudesC)
    % read from resp
    fileNameC = strcat('data/KFS/CFibre', sprintf("%.1f",frequency/1e3), 'kHz', sprintf("%.1f",amplitudesC(i)), 'uA.txt');
    respC = readmatrix(fileNameC);

    % get firing rate
    srC = firingRate(respC);
    SRC = [SRC, srC];
end

figure; hold on;
plot(amplitudesC, SRC, 'Color', [0.9290 0.6940 0.1250], 'linewidth', linewidth);
xlabel('amplitude (uA)');
ylabel('NSR');
ylim([-4 10]);


%% AP plot for C fibre
frequency = 4e3;
amplitude = 600;

% read from resp
fileNameC = strcat('data/KFS/CFibre', sprintf("%.1f",frequency/1e3), 'kHz', sprintf("%.1f",amplitude), 'uA.txt');
respC = readmatrix(fileNameC);

figure; hold on;
plot(respC, 'Color', [0.9290 0.6940 0.1250], 'linewidth', linewidth);
xlabel('amplitude (uA)');
ylabel('NSR');
ylim([-100 60]);