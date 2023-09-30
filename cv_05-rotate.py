import cv2 as cv
import numpy as np
import imutils

blocks = cv.imread('/Users/jasen_levoy/Documents/Projects/PlotBot/PicknPlace/alpha_blocks_a-30b.jpg',1)
imGray = cv.cvtColor(blocks, cv.COLOR_BGR2GRAY)
cv.imshow('imGray',imGray)
template = cv.imread("alpha_blocks_a-level.jpg", 0)
rot_30 = cv.imread("/Users/jasen_levoy/Documents/Projects/PlotBot/PicknPlace/A-Rot/A-Rot_30.jpg",0)
cv.imshow('template',template)
temp = 0

"""
res = cv.matchTemplate(imGray, template, cv.TM_CCOEFF_NORMED)
print("res max ",res.max())
threshold = 0.98
location = np.where(res >= threshold)
for pt in zip(*location[::-1]):
    cv.rectangle(blocks, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), (2))
"""

for angle in range(0,375,15):
    rotated = imutils.rotate_bound(template, angle)
    w, h = rotated.shape[::-1]
    cv.imwrite("/Users/jasen_levoy/Documents/Projects/PlotBot/PicknPlace/A-Rot/A-Rot_" + str(angle) + ".jpg", rotated)
    res = cv.matchTemplate(imGray, rotated, cv.TM_CCOEFF_NORMED)
    threshold = 0.98
    location = np.where(res >= threshold)
    print("res max ",res.max())
#        temp = angle
    print("location", location)
    print("template ", w, " ", h)
    print("res ",res)
    print("angle ",angle)
    for pt in zip(*location[::-1]):
        cv.rectangle(blocks, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), (2))

cv.imshow('blocks',blocks)
cv.imshow('rot_30',rot_30)
cv.imshow('rotated', rotated)
#cv.imshow('template', template)
cv.waitKey(0)
cv.destroyAllWindows()
