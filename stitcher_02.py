######## Resources ###########
# 1 : https://docs.opencv.org/3.1.0/dc/dc3/tutorial_py_matcher.html
# 2 : https://stackoverflow.com/questions/42538914/why-is-ransac-not-working-for-my-code
# 3 : https://docs.opencv.org/3.1.0/d6/d00/tutorial_py_root.html


import cv2
import numpy as np
import matplotlib.pyplot as plt
from random import randrange

path = "/Users/jasen_levoy/Documents/Projects/PlotBot/PicknPlace/"

img_ = cv2.imread(path+'blocks_stitch_02.jpg')    #right
img1 = cv2.cvtColor(img_,cv2.COLOR_BGR2GRAY)

img = cv2.imread(path+'blocks_stitch_01.jpg')   #left
img2 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


sift = cv2.xfeatures2d.SIFT_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)
# BFMatcher with default params
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2, k=2) 

#print matches
# Apply ratio test
good = []
for m in matches:
     if m[0].distance < 0.5*m[1].distance:         
     	good.append(m)
matches = np.asarray(good)
 	 

'''print matches[2,0].queryIdx
print matches[2,0].trainIdx
print matches[2,0].distance'''


if len(matches[:,0]) >= 4:
    src = np.float32([ kp1[m.queryIdx].pt for m in matches[:,0] ]).reshape(-1,1,2)
    dst = np.float32([ kp2[m.trainIdx].pt for m in matches[:,0] ]).reshape(-1,1,2)

    H, masked = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
    print(H)
else:
    raise AssertionError("Can't find enough keypoints.")  	
   
dst = cv2.warpPerspective(img_,H,(img.shape[1] + img_.shape[1], img.shape[0]))     	
plt.subplot(122),plt.imshow(dst),plt.title('Warped Image')
plt.show()
plt.figure()
dst[0:img.shape[0], 0:img.shape[1]] = img
cv2.imwrite(path+'resultant_stitched_panorama.jpg',dst)
cv2.imshow('dst may be result',dst)
plt.imshow(dst)
plt.show()
cv2.imwrite(path+'resultant_stitched_panorama.jpg',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
