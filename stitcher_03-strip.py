import cv2 as cv
import numpy as np

path = "/Users/jasen_levoy/Documents/Projects/PlotBot/PicknPlace/blocks_stitch_raw/"

j_start=1460    #dist removed in from left edge src
i_start=0    #dist removed down from top of src
j_end=1830   #dist included in from left edge src
i_end=2448   #dist included down from top of src 

for i in range(8):
	src = cv.imread(path+'stitch_raw_0'+str(i+1)+'.JPG')
	dst = src[i_start:i_end, j_start:j_end]
	cv.imwrite(path+'stitch_strip_0'+str(i+1)+'.JPG', dst)

img1 = cv.imread(path+'stitch_strip_01.JPG')
img2 = cv.imread(path+'stitch_strip_02.JPG')
img3 = cv.imread(path+'stitch_strip_03.JPG')
img4 = cv.imread(path+'stitch_strip_04.JPG')
img5 = cv.imread(path+'stitch_strip_05.JPG')
img6 = cv.imread(path+'stitch_strip_06.JPG')
img7 = cv.imread(path+'stitch_strip_07.JPG')
img8 = cv.imread(path+'stitch_strip_08.JPG')

concat = cv.hconcat([img8,img7,img6,img5,img4,img3,img2,img1])
cv.imwrite(path+'stitched.JPG', concat)


#src = cv.imread(path+'stitch_calib.JPG');
#dst = src[i_start:i_end, j_start:j_end]
#cv.imwrite(path+'stitch_calib_done.JPG', dst)
#cv.imshow('calib',dst)
#cv.waitKey(0)
#cv.destroyAllWindows()

#src.delete()
#dst.delete()
