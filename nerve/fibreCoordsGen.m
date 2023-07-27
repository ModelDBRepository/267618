% This MATLAB script generates non-overlapping fibres in the sciatic nerve.

clc; clear;

fname = 'sciaticNerveCoords.txt';
fileID = fopen(fname, 'w');

rng(1);

largeFascD = 1000;           % large fascicle diameter 
nFibreLarge = 150;           % number of fibres within a large fascicle
mediumFascD = 600;           % medium fascicle diameter
nFibreMedium = 90;           % number of fibres within a medium fascicle
smallFascD = 300;            % small fascicle diameter
nFibreSmall = 45;            % number of fibres within a small fascicle

% Create large fascicles
createFascicle(-1250, 750, largeFascD, nFibreLarge, fileID)
createFascicle(200, 840, largeFascD, nFibreLarge, fileID)
createFascicle(1000, -1000, largeFascD, nFibreLarge, fileID)

% create medium fascicles
createFascicle(950, 1400, mediumFascD, nFibreMedium, fileID) 
createFascicle(0, 0, mediumFascD, nFibreMedium, fileID)
createFascicle(0, -1500, mediumFascD, nFibreMedium, fileID)
createFascicle(-900, -1100, mediumFascD, nFibreMedium, fileID)
createFascicle(0, 1680, mediumFascD, nFibreMedium, fileID)

% create small fascicles
createFascicle(-600, 1650, smallFascD, nFibreSmall, fileID)
createFascicle(-700, 1300, smallFascD, nFibreSmall, fileID)
createFascicle(-1500, 0, smallFascD, nFibreSmall, fileID)
createFascicle(1500, 0, smallFascD, nFibreSmall, fileID)
createFascicle(-1400, -600, smallFascD, nFibreSmall, fileID)
createFascicle(-1000, -400, smallFascD, nFibreSmall, fileID)

function createFascicle(fasCenterX, fasCenterY, dFasc, nFibres, fileID)
    nCircles = nFibres;
    rFasc = dFasc/2;
    circles = zeros(nCircles ,2);
    rFibre = 6; % keep-out distance between adjacent fibres

    % open file
    if rFasc == 150
        fascSize = 'sml';
    elseif rFasc == 300
        fascSize = 'med';
    else 
        fascSize = 'big';
    end
    
    for i = 1 : nCircles
        % flag which holds true whenever a new circle was found
        newCircleFound = false;
        
        % loop iteration which runs until finding a circle which doesnt intersect with previous ones
        while ~newCircleFound
            r = (rFasc-10) * sqrt(rand(1));
            theta = rand(1) * 2 * pi; 
            x = fasCenterX + r*cos(theta);
            y = fasCenterY + r*sin(theta);
            
            % calculates distances from previous drawn circles
            prevCirclesY = circles(1:i-1, 1);
            prevCirclesX = circles(1:i-1, 2);
            distFromPrevCircles = ((prevCirclesX-x).^2 + (prevCirclesY-y).^2).^0.5;
            
            % if the distance is not to small - adds the new circle to the list
            if i==1 || sum(distFromPrevCircles<=2*rFibre)==0
                newCircleFound = true;
                circles(i,:) = [y x];
                circle3(x,y,rFibre);
                % write coordinate to file
                fprintf(fileID, "%g %g\n", x, y);
            end
        
        end
        hold on
    end
end

function h = circle3(x,y,r)
    d = r*2;
    px = x-r;
    py = y-r;
    h = rectangle('Position',[px py d d],'Curvature',[1,1]);
    daspect([1,1,1]);
end