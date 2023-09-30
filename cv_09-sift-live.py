import cv2
import math

# changed min match count from 10 to 30
MIN_MATCH_COUNT = 5

path = "/Users/jasen_levoy/Documents/Projects/PlotBot/PicknPlace/"

result_path = "/Users/jasen_levoy/Documents/Projects/PlotBot/PicknPlace/Live_Result/"

query_image_fn = path+"alpha_blocks_a_live.png"  #query = template
train_image_fn = path+"alpha_blocks_live.png"  #train = field

img1 = cv2.imread(query_image_fn, cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread(train_image_fn, cv2.IMREAD_GRAYSCALE)
#th_val, img1_th = cv2.threshold(img1_raw, 80, 255, cv2.THRESH_BINARY)  #template binary threshold
#th_val, img2_th = cv2.threshold(img2_raw, 80, 255, cv2.THRESH_BINARY)  #field binary threshold
#img1 = cv2.Canny(img1_raw,50,255)
#img2 = cv2.Canny(img2_raw,50,255)
img1 = cv2.pyrDown(img1)
img1 = cv2.pyrDown(img1)
img2 = cv2.pyrDown(img2)
img2 = cv2.pyrDown(img2)
#cv2.imshow('img1 threshold',img1)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#cv2.imshow('img2 threshold',img2)
#cv2.waitKey(0)
#cv2.destroyAllWindows()


#orb = cv2.ORB_create(10000, 1.2, nlevels=8, edgeThreshold = 5)

# find the keypoints and descriptors with ORB
#kp1, des1 = orb.detectAndCompute(img1, None)
#kp2, des2 = orb.detectAndCompute(img2, None)

sift = cv2.xfeatures2d.SIFT_create()

kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth

x = np.array([kp2[0].pt])

for i in range(len(kp2)):
    x = np.append(x, [kp2[i].pt], axis=0)

x = x[1:len(x)]

bandwidth = estimate_bandwidth(x, quantile=0.1, n_samples=500)

ms = MeanShift(bandwidth=bandwidth, bin_seeding=True, cluster_all=True)
ms.fit(x)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)
#print("number of estimated clusters : %d" % n_clusters_)

s = [None] * n_clusters_
for i in range(n_clusters_):
    l = ms.labels_
    d, = np.where(l == i)
    #print(d.__len__())
    s[i] = list(kp2[xx] for xx in d)

des2_ = des2

img_inc = 0

for i in range(n_clusters_):

    kp2 = s[i]
    l = ms.labels_
    d, = np.where(l == i)
    des2 = des2_[d, ]

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    des1 = np.float32(des1)
    des2 = np.float32(des2)

    matches = flann.knnMatch(des1, des2, 2)


    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)

    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        # stack has 2 at the end, but other guides use 5
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5)

        if M is None:
            print ("No Homography")
        else:
            matchesMask = mask.ravel().tolist()

            h,w = img1.shape
            pts = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2) 
            
            
            # calculate angle
            # handle skew with SVD decomposition
            #u, _, vh = np.linalg.svd(M[0:2, 0:2])
            #R = u @ vh
            #theta = - math.atan2(R[0,1], R[0,0]) * 180 / math.pi
            
            theta = -math.atan2(M[0,1], M[0,0]) * 180 / math.pi

            print("angle:", round((theta),0))

            dst = cv2.perspectiveTransform(pts,M)

            border_shade = 0

            # img2 = cv2.polylines(img2,[np.int32(dst)],True,  border_shade  ,3, cv2.LINE_AA)

            img2 = cv2.polylines(img2,[np.int32(dst)],True,  border_shade  ,3, cv2.LINE_AA)

            draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                               singlePointColor=(255, 0, 0),
                               matchesMask=matchesMask,  # draw only inliers
                               flags=2)

            img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)

            img_inc += 1
            cv2.imwrite(result_path+'Block_Matches_inc{}.png'.format(img_inc), img3)
            cv2.imwrite(result_path+'Block_Matches.png'.format(img_inc), img2)
            #print(dst)
            print('x,y: ',(round(((dst[0][0][0]+dst[2][0][0])/2),0),round(((dst[0][0][1]+dst[2][0][1])/2),0)))
            print()

    else:
        #print ("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
        matchesMask = None