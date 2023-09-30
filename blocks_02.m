%% Find Image Rotation and Scale Using Automated Feature Matching
% This example shows how to automatically determine the geometric
% transformation between a pair of images. When one image is distorted
% relative to another by rotation and scale, use |detectSURFFeatures| and
% |estimateGeometricTransform2D| to find the rotation angle and scale factor.
% You can then transform the distorted image to recover the original image.

% Copyright 1993-2007 The MathWorks, Inc. 
clear;
%% Step 1: Read Image
% Bring an image into the workspace.
template = imread('sample_images/blocks_template_a.jpg');
%imshow(template)
%text(size(template,2),size(template,1)+15, ...
%    'blocks\_template\_a', ...
%    'FontSize',12,'HorizontalAlignment','right');
src = imread('sample_images/blocks_bk_dst_08.jpg');

%% Step 2: Resize and Rotate the Image
%scale = 0.7;
%J = imresize(template, scale); % Try varying the scale factor.

%theta = 30;
%distorted = imrotate(J,theta); % Try varying the angle, theta.
%figure(2) 
%imshow(distorted)

%%
% You can experiment by varying the scale and rotation of the input image.
% However, note that there is a limit to the amount you can vary the scale
% before the feature detector fails to find enough features.

%% Step 3: Find Matching Features Between Images
% Detect features in both images.
ptsTemplate  = detectSURFFeatures(template);
ptsSrc = detectSURFFeatures(src);

%%
% Extract feature descriptors.
[featuresTemplate,  validPtsTemplate]  = extractFeatures(template,  ptsTemplate);
[featuresSrc, validPtsSrc] = extractFeatures(src, ptsSrc);

%%
% Match features by using their descriptors.
indexPairs = matchFeatures(featuresTemplate, featuresSrc);

%%
% Retrieve locations of corresponding points for each image.
matchedTemplate  = validPtsTemplate(indexPairs(:,1));
matchedSrc = validPtsSrc(indexPairs(:,2));

%%
% Show putative point matches.
%figure;
% showMatchedFeatures(template,src,matchedTemplate,matchedSrc);
% title('Putatively matched points (including outliers)');

%% Step 4: Estimate Transformation
% Find a transformation corresponding to the matching point pairs using the
% statistically robust M-estimator SAmple Consensus (MSAC) algorithm, which
% is a variant of the RANSAC algorithm. It removes outliers while computing
% the transformation matrix. You may see varying results of the
% transformation computation because of the random sampling employed by the
% MSAC algorithm.
[tform, inlierIdx] = estimateGeometricTransform2D(...
    matchedSrc, matchedTemplate, 'similarity');
inlierSrc = matchedSrc(inlierIdx, :);
inlierTemplate  = matchedTemplate(inlierIdx, :);


%% Step 5: Solve for Scale and Angle
% Use the geometric transform, tform, to recover the scale and angle.
% Since we computed the transformation from the src to the template
% image, we need to compute its inverse to recover the distortion.
%
%  Let sc = s*cos(theta)
%  Let ss = s*sin(theta)
%
%  Then, Tinv = [sc -ss  0;
%                ss  sc  0;
%                tx  ty  1]
%
%  where tx and ty are x and y translations, respectively.
%

%%
% Compute the inverse transformation matrix.
Tinv  = tform.invert.T

ss = Tinv(2,1)
sc = Tinv(1,1)
scaleRecovered = sqrt(ss*ss + sc*sc)
thetaRecovered = atan2(ss,sc)*180/pi

%%
% The recovered values should match your scale and angle values selected in
% *Step 2: Resize and Rotate the Image*.

%% Step 6: Recover the Original Image
% Recover the original image by transforming the src image.
outputView = imref2d(size(template));
recovered  = imwarp(src,tform,'OutputView',outputView);
%%
% Display matching point pairs used in the computation of the
% transformation.
tx = Tinv(3,1)
ty = Tinv(3,2)
%tx = tform.T(3,1)
%ty = tform.T(3,2)
figure; 
hold on
showMatchedFeatures(template,src,inlierTemplate,inlierSrc);
title('Matching points (inliers only)');
legend('ptsTemplate','ptsSrc');

theta = -1*thetaRecovered;
theta = theta + 45;
theta = theta*pi/180;
nintey = 90*pi/180;
threeFifteen = 315*pi/180;
r = 50;
adjust = 103;
tx = tx + adjust*cosd(thetaRecovered-45);
ty = ty - adjust*sind(thetaRecovered-45);
center = [tx, ty];

tr_x = center(1,1) + r*cos(theta);
tr_y = center(1,2) + r*sin(theta);

tl_x = center(1,1) + r*cos(theta+nintey);
tl_y = center(1,2) + r*sin(theta+nintey);

bl_x = center(1,1) + r*cos(theta+nintey*2);
bl_y = center(1,2) + r*sin(theta+nintey*2);

br_x = center(1,1) + r*cos(theta+nintey*3);
br_y = center(1,2) + r*sin(theta+nintey*3);

line([tr_x tl_x], [tr_y tl_y], 'color','g','lineWidth', 3)
line([br_x bl_x], [br_y bl_y], 'color','r','lineWidth', 3)
line([tr_x br_x], [tr_y br_y], 'color','b','lineWidth', 3)
line([tl_x bl_x], [tl_y bl_y], 'color','y','lineWidth', 3)
% rectangle('Position', [tx, ty, 150, 150],...
%   'EdgeColor','g', 'LineWidth', 3)
%%
% Compare |recovered| to |original| by looking at them side-by-side in a
% montage.
%figure, imshowpair(template,recovered,'montage')

%%
% The |recovered| (right) image quality does not match the |original|
% (left) image because of the distortion and recovery process. In
% particular, the image shrinking causes loss of information. The artifacts
% around the edges are due to the limited accuracy of the transformation.
% If you were to detect more points in *Step 3: Find Matching Features
% Between Images*, the transformation would be more accurate. For example,
% we could have used a corner detector, detectFASTFeatures, to complement
% the SURF feature detector which finds blobs. Image content and image size
% also impact the number of detected features.
