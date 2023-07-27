clc; clear;


%% read stim info from the whole nerve for monopolar setup
fid = fopen('data/PE/mono.txt');
stimInfo = textscan(fid, '%s %s %s %s');

% extract stim info
Name = stimInfo(:,1);
Name = Name{1}';

Y = stimInfo(:,2);
Y = [cellfun(@str2num,Y{1},'un',0).'];
Y = cell2mat(Y);

Z = stimInfo(:,3);
Z = [cellfun(@str2num,Z{1},'un',0).'];
Z = cell2mat(Z);

SR = stimInfo(:,4);
SR = [cellfun(@str2num,SR{1},'un',0).'];
SR = cell2mat(SR);

% plot nerve cross section
N = size(SR, 2);
figure; hold on;
markerSize = 400;
for i = 1:N
    fiberName = Name{i}(1:6);
    faceColor = 'white';
    linewidth = 0.01;
    % determine fiber type
    if strcmp(fiberName, 'AFibre')
        marker = 'o';
        color = 'black';
        % determine activity
        if SR(i) > 3
            faceColor = 'red';
            linewidth = 0.01;
        elseif SR(i) > 0 && SR(i) < 3
            faceColor = 'yellow';
            linewidth = 0.01;
        end
    else
        marker = '+';
        color = 'white';
        linewidth = 5;
        % determine activity
        if SR(i) > 0
            color = 'green';
        end
    end
    scatter(Y(i), Z(i), markerSize, marker, color, 'MarkerFaceColor', faceColor, 'linewidth', linewidth);
end

set(gca,'Color','k')


%% read stim info from the whole nerve for hexapolar setup
fid = fopen('data/PE/hex.txt');
stimInfo = textscan(fid, '%s %s %s %s');

% extract stim info
Name = stimInfo(:,1);
Name = Name{1}';

Y = stimInfo(:,2);
Y = [cellfun(@str2num,Y{1},'un',0).'];
Y = cell2mat(Y);

Z = stimInfo(:,3);
Z = [cellfun(@str2num,Z{1},'un',0).'];
Z = cell2mat(Z);

SR = stimInfo(:,4);
SR = [cellfun(@str2num,SR{1},'un',0).'];
SR = cell2mat(SR);

% plot nerve cross section
N = size(SR, 2);
figure; hold on;
markerSize = 400;
for i = 1:N
    fiberName = Name{i}(1:6);
    faceColor = 'white';
    linewidth = 0.01;
    % determine fiber type
    if strcmp(fiberName, 'AFibre')
        marker = 'o';
        color = 'black';
        % determine activity
        if SR(i) > 3
            faceColor = 'red';
            linewidth = 0.01;
        elseif SR(i) > 0 && SR(i) < 3
            faceColor = 'yellow';
            linewidth = 0.01;
        end
    else
        marker = '+';
        color = 'white';
        linewidth = 5;
        % determine activity
        if SR(i) > 0
            color = 'green';
        end
    end
    scatter(Y(i), Z(i), markerSize, marker, color, 'MarkerFaceColor', faceColor, 'linewidth', linewidth);
end

set(gca,'Color','k')