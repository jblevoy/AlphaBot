import cv2 as cv

shapes = cv.imread('/Users/jasen_levoy/Documents/Projects/PlotBot/PicknPlace/color_shapes.jpg', -1)
imGray = cv.cvtColor(shapes, cv.COLOR_BGR2GRAY)
_, thresh = cv.threshold(imGray, 230, 255, cv.THRESH_BINARY)
contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

for contour in contours:
    approx=cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
    cv.drawContours(shapes, [approx], 0, (0,0,0), 2)
    x = approx.ravel()[0] -5 #ravel captures location
    y = approx.ravel()[1] -10 #y seems to be inverted, think i,j

    if len(approx) == 3:
        cv.putText(shapes, "Triangle", (x,y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0))
    if len(approx) == 4:
        cv.putText(shapes, "Square", (x,y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0))
    if len(approx) == 10:
        cv.putText(shapes, "Star", (x,y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0))
    if len(approx) > 10:
        cv.putText(shapes, "Circle", (x,y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0))

print(shapes)

cv.imshow('image', shapes)
cv.waitKey(0)
cv.destroyAllWindows()
