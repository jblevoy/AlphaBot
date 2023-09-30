rgbImage=imread('sample_images/blocks_bk_src.tif');
imshow(rgbImage)

%line([500 200], [30 30])
%hold on
%rectangle('Position', [203, 147, 218, 162],...
 % 'EdgeColor','r', 'LineWidth', 3)
bbox = [50 20 200 50];

X = [bbox(1), bbox(1), bbox(1)+bbox(3), bbox(1)+bbox(3), bbox(1)];
Y = [bbox(2), bbox(2)+bbox(4), bbox(2)+bbox(4), bbox(2), bbox(2)];
%Rotation always rotates around the origin (0,0), if you want to rotate around the center of the box you need to adjust X and Y before and after the rotation

Cx = bbox(1)+0.5*bbox(3);
Cy = bbox(2)+0.5*bbox(4);
%Rotating

Xr = X-Xc; %// subtract center
Yr = Y-Cy;
Xr = cosd(30)*Xr-sind(30)*Yr; %// rotate
Yr = sind(30)*Xr+cosd(30)*Yr;
Xr = Xr+Xc; %// add center back
Yr = Yr+Yc;
%Now you can plot the rotated box

plot( Xr, Yr );

