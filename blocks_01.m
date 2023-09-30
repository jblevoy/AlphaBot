%Detect features in both images.
ptsOriginal  = detectSURFFeatures(original);
ptsDistorted = detectSURFFeatures(distorted);

%Extract feature descriptors.
[featuresOriginal,  validPtsOriginal]  = extractFeatures(original,  ptsOriginal);
[featuresDistorted, validPtsDistorted] = extractFeatures(distorted, ptsDistorted);

%Match features by using their descriptors.
indexPairs = matchFeatures(featuresOriginal, featuresDistorted);

% Retrieve locations of corresponding points for each image.
matchedOriginal  = validPtsOriginal(indexPairs(:,1));
matchedDistorted = validPtsDistorted(indexPairs(:,2));

%Show putative point matches.
figure;
showMatchedFeatures(original,distorted,matchedOriginal,matchedDistorted);
title('Putatively matched points (including outliers)');

%transformation estimation
[tform, inlierIdx] = estimateGeometricTransform2D(...
    matchedDistorted, matchedOriginal, 'similarity');
inlierDistorted = matchedDistorted(inlierIdx, :);
inlierOriginal  = matchedOriginal(inlierIdx, :);

%Display matching point pairs used in the computation of the transformation.
figure;
showMatchedFeatures(original,distorted,inlierOriginal,inlierDistorted);
title('Matching points (inliers only)');
legend('ptsOriginal','ptsDistorted');


%compute inverse transformation matrix
% Tinv  = tform.invert.T;
% 
% ss = Tinv(2,1);
% sc = Tinv(1,1);
% scaleRecovered = sqrt(ss*ss + sc*sc)
% thetaRecovered = atan2(ss,sc)*180/pi
