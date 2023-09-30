import cv2 as cv

shapes = cv.imread('/Users/jasen_levoy/Documents/Projects/PlotBot/PicknPlace/shapes.jpg', 0)
print(shapes)

cv.imshow('image', shapes)
cv.waitKey(0)
cv.destroyAllWindows()
