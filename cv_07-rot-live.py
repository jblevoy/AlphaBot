import cv2 as cv
import numpy as np
import imutils

field = cv.imread('/Users/jasen_levoy/Documents/Projects/PlotBot/PicknPlace/alpha_blocks_live.JPG',1) #30 deg and -15 deg 2 deg white background
field = cv.pyrDown(field)
field = cv.pyrDown(field)
field_gs = cv.cvtColor(field, cv.COLOR_BGR2GRAY)   #field_gs = gray scale
th_val, field_bin = cv.threshold(field_gs, 120, 255, cv.THRESH_BINARY)  #field binary threshold
cv.imwrite('blocks_live_th_result.JPG',field_bin)
i=0
A =[]

"""
a = cv.imread("alpha_blocks_a_live.jpg", 1)
a = cv.pyrDown(a)
a_gs = cv.cvtColor(a, cv.COLOR_BGR2GRAY)  
th_val, a_inv = cv.threshold(a_gs, 180, 255, cv.THRESH_BINARY)  #a_inv = 'a' template threshold + inverse
cv.imshow('a_inv',a_inv)


for angle in range(0,360,1):
    a_inv_rot = imutils.rotate_bound(a_inv, angle)
    w, h = a_inv_rot.shape[::-1]
    a_rot = cv.bitwise_not(a_inv_rot)      
    #cv.imwrite("/Users/jasen_levoy/Documents/Projects/PlotBot/PicknPlace/A-Rot/A-Rot_" + str(angle) + ".jpg", temp_rot)
    res = cv.matchTemplate(field_bin, a_rot, cv.TM_CCOEFF_NORMED)
    threshold = 0.95
    location = np.where(res >= threshold)
    #print("res max ",res.max())
    #print("location", location)
    #print("template ", w, " ", h)
    #print("res ",res)
    #print("angle ",angle)
    for pt in zip(*location[::-1]):
        A.append([1,0,0,0,0])
        cv.rectangle(field, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), (2))
        x = pt[0]
        y = pt[1]
        #print('y,x: ',y,x)
        #print('res y x ',res[y][x])
        A[i][1] = x
        A[i][2] = y
        A[i][3] = angle
        A[i][4] = res[y][x]
        i+=1

b = cv.imread("alpha_blocks_b_live.jpg", 1)
b = cv.pyrDown(b)
b_gs = cv.cvtColor(b, cv.COLOR_BGR2GRAY)  
th_val, b_inv = cv.threshold(b_gs, 180, 255, cv.THRESH_BINARY_INV)  #temp_th_inv = template threshold inverse

for angle in range(0,360,1):
    b_inv_rot = imutils.rotate_bound(b_inv, angle)
    w, h = b_inv_rot.shape[::-1]
    b_rot = cv.bitwise_not(b_inv_rot)      
    #cv.imwrite("/Users/jasen_levoy/Documents/Projects/PlotBot/PicknPlace/A-Rot/A-Rot_" + str(angle) + ".jpg", temp_rot)
    res = cv.matchTemplate(field_bin, b_rot, cv.TM_CCOEFF_NORMED)
    threshold = 0.95
    location = np.where(res >= threshold)
    #print("res max ",res.max())
    #print("location", location)
    #print("template ", w, " ", h)
    #print("res ",res)
    #print("angle ",angle)
    for pt in zip(*location[::-1]):
        A.append([2,0,0,0,0])
        cv.rectangle(field, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), (2))
        x = pt[0]
        y = pt[1]
        A[i][1] = x
        A[i][2] = y
        A[i][3] = angle
        A[i][4] = res[y][x]
        i+=1


#put together all physical block batches eg rejoin 0deg and 360 deg matches of the same block 
A_match = []
A_group =[]
A_break_index = []
A_best =[]
for i, j in enumerate(A):
    for k,l in enumerate(A):
        if abs(A[i][1] - A[k][1]) <= 5 and abs(A[i][2] - A[k][2]) <= 5:
            A_match.append(A[k])
#eliminate duplication
A_match = [x for n, x in enumerate(A_match) if x not in A_match[:n]]
#create A_break_index which is a list of the indecies in A_match just before the index where a new blocks matches begin
for i,j in enumerate(A_match):
    try:
        if abs(A_match[i][1] - A_match[i+1][1]) >= 5 and abs(A_match[i][2] - A_match[i+1][2]) >= 5 and i+1 <= len(A_match):
            A_break_index.append(int(i))
    except:
        pass   

#use A_break_index to create a new temp list A_group to group just matches of same block, then select highest fit among them and add only that match to A_best
count=0
A_break_index.append(len(A_match)-1)
for i,j in enumerate(A_break_index):
    while count <= A_break_index[i]:
        A_group.append(A_match[count])
        count+=1   
    A_group.sort(key = lambda x: x[4])
    A_group.reverse()
    A_best.append(A_group[0])
    A_group = []


#print('A_match: ',A_match)
#print('A_group: ',A_group)
#print('A_break_index: ',A_break_index)
print('A_best: ',A_best)

#print()
#print('A', A)
"""

cv.imshow('field',field)
#cv.imshow('a rot ',a_rot)
#cv.imshow('b rot ',b_rot)
#cv.imshow('rotated', rotated)
#print('angle: ',

cv.waitKey(0)
cv.destroyAllWindows()









