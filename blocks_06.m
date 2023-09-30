clear;
rgbImage=imread('sample_images/blocks_bk_src.tif');
imshow(rgbImage)

theta = 13;
theta = theta + 45;
theta = theta*pi/180;
nintey = 90*pi/180;
r = 80;
adjust = 80;
center = [563, 402]; 

%center = [563 + adjust*cos(theta+nintey*3), 402 - adjust*sin(theta+nintey*3)];
%slope = center(1,2)

tr_x = center(1,1) + r*cos(theta);
tr_y = center(1,2) + r*sin(theta);

tl_x = center(1,1) + r*cos(theta+nintey);
tl_y = center(1,2) + r*sin(theta+nintey);

bl_x = center(1,1) + r*cos(theta+nintey*2);
bl_y = center(1,2) + r*sin(theta+nintey*2);

br_x = center(1,1) + r*cos(theta+nintey*3);
br_y = center(1,2) + r*sin(theta+nintey*3);

line([tr_x tl_x], [tr_y tl_y], 'color','g','lineWidth', 3)
line([br_x bl_x], [br_y bl_y], 'color','b','lineWidth', 3)
line([tr_x br_x], [tr_y br_y], 'color','r','lineWidth', 3)
line([tl_x bl_x], [tl_y bl_y], 'color','y','lineWidth', 3)
line([center(1,1) tr_x], [center(1,2), tr_y], 'color','g','lineWidth', 3);

% hold on
%rectangle('Position', [203, 147, 218, 162],...
%'EdgeColor','r', 'LineWidth', 3)
% 
% tr_x
% tr_y
% tl_x
% tl_y
% bl_x
% bl_y
% br_x
% br_y