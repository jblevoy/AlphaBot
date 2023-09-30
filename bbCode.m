%% Plot bounding box
boundingBox = bb(boundBox, itr);
x1 = boundingBox(1);
y1 = boundingBox(2);
x2 = x1 + boundingBox(3)-1;
y2 = y1 + boundingBox(4)-1;
verticesX = [x1 x2 x2 x1 x1];
verticesY = [y1 y1 y2 y2 y1];
verticesXY = [verticesX; verticesY];
p1 = plot(verticesX, verticesY, 'r-', 'LineWidth', 2); 

%% Create the hgtransform objects and parent them to the same axes
t1 = hgtransform('Parent',gca);
t2 = hgtransform('Parent',gca);

%% Parent the plots to hgtransform t1, then copy the objects and parent the copies to hgtransform t2
set(p1,'Parent',t1)
p2 = copyobj(p1,t2);

%% Rotate the first object
Rz = makehgtform('zrotate', rot_angle_rad); % Assign value to the variable rot_angle_rad
set(t1,'Matrix',Rz);

%% Translate and rotate the second hgtransform object

% Assign values to the variable opp_side_x and opp_side_y and rot_angle_rad
% in radians
Txy = makehgtform('translate',[opp_side_x opp_side_y 0], 'zrotate', rot_angle_rad); 
set(t2,'Matrix',Txy);

drawnow;

 
