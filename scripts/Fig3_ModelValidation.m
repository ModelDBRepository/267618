clc; clear;
linewidth = 5;


%% A fibre response

% read from A fibre resp
fileNameA = strcat('data/modelValidation/AFibreModelValidation.txt');
respA = readmatrix(fileNameA);
respA = reshape(respA, [size(respA,1)/3,3]);
T = linspace(0, 160, size(respA,1));

% plot resp
figure; hold on;
plot(T, respA(:,3), 'linewidth', linewidth);
plot(T, respA(:,2), 'linewidth', linewidth);
plot(T, respA(:,1), 'linewidth', linewidth);
ylim([-85, -50]);


%% C fibre response

% read from A fibre resp
fileNameC = strcat('data/modelValidation/CFibreModelValidation.txt');
respC = readmatrix(fileNameC);
respC = reshape(respC, [size(respC,1)/3,3]);
T = linspace(0, 160, size(respC,1));

% plot resp
figure; hold on;
plot(T, respC(:,3), 'linewidth', linewidth);
plot(T, respC(:,2), 'linewidth', linewidth);
plot(T, respC(:,1), 'linewidth', linewidth);
ylim([-85, 50]);