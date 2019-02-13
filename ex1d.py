from tempfile import TemporaryFile
import numpy as np
from pylab import imshow, figure
import matplotlib.pyplot as plt
import cv2

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# function
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def recursive_ver(mat,ver_len,i_h, j_w, path_array_i, path_array_j):
    h = len(mat)
    w = len(mat[0])
    if((i_h+1== h)or(j_w+1 == w)or(i_h==0)or(j_w==0)):
        return ver_len

    #black row
    if((mat[i_h+1][j_w -1] ==0)and(mat[i_h+1][j_w +1]==0) and (mat[i_h+1][j_w]==0)):
        return recursive_ver(mat,ver_len,i_h+1,j_w,path_array_i,path_array_j)

    x=0
    y=0
    z=0
    if(mat[i_h+1][j_w]):
        x = recursive_ver(mat, ver_len+1,i_h+1,j_w ,path_array_i,path_array_j)
    elif(mat[i_h+1][j_w -1]):
        y = recursive_ver(mat, ver_len+1,i_h+1,j_w -1,path_array_i,path_array_j)
    elif(mat[i_h+1][j_w+1]):
        z = recursive_ver(mat, ver_len+1,i_h+1,j_w+1,path_array_i,path_array_j)

    if((x>=y)and(x>=z)):
        path_array_i.append(i_h+1)
        path_array_j.append(j_w)
        return x
    if((y>=x)and(y>=z)):
        path_array_i.append(i_h+1)
        path_array_j.append(j_w-1)
        return y
    if((z>=y)and(z>=x)):
        path_array_i.append(i_h+1)
        path_array_j.append(j_w+1)
        return z

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# find_line
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def find_line(src_img):
    # src_img = cv2.imread('sudoku-original.jpg',0)
    h = len(src_img)
    w = len(src_img[0])

    #print src image
    # plt.imshow(src_img, cmap = 'gray')



    #dilation
    dilate = cv2.filter2D(src_img, -1,
    np.array([[1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]]))

    max_len = 0
    new_img = np.zeros((h, w))

    #find vertical cols
    for x in range(1, w):
        array_i =[]
        array_j =[]
        len_ = recursive_ver(dilate,0,1,x,array_i,array_j)
        if(len_>= h/2):
            point = 0
            count = 0
            max_count = 0
            max_point = 0
            for y in range(1, len(array_i)):
                if((array_i[y-1]-array_i[y])==1):
                    count=count+1
                else:
                    if(count > max_count):
                        max_count=count
                        max_point=point
                    point = y
                    count = 0
            if(count > max_count):
                max_count=count
                max_point=point
            for z in range(max_point, max_count + max_point):
                new_img[array_i[z]][array_j[z]]=255


    #to see better
    new_img = cv2.filter2D(new_img, -1,
    np.array([[1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1]]))

    threshold_i = (new_img > 255) * 255
    threshold_i = threshold_i.astype(np.uint8)

    # plt.figure("vertical cols - white:black")
    # plt.imshow(threshold_i, cmap = 'gray')
    # plt.figure("vertical cols - black:white")
    # plt.imshow(~threshold_i, cmap = 'gray')
    # plt.figure("vertical cols on src_img")
    # plt.imshow(~threshold_i+src_img, cmap = 'gray')

    colsColor = cv2.cvtColor(threshold_i,cv2.COLOR_GRAY2RGB)
    srcImgColor = cv2.cvtColor(src_img,cv2.COLOR_GRAY2RGB)


    b,g,r = cv2.split(colsColor)
    g = np.zeros((h, w))
    b = np.zeros((h, w))
    redImg = np.dstack((r,g,b))
    redImg = (redImg).astype(np.uint8)

    # plt.figure("red cols")
    # plt.imshow(redImg)

    src_with_red_cols = srcImgColor
    for x in range(0,h):
        for y in range(0,w):
            if(redImg[x][y][0]):
                src_with_red_cols[x][y] = redImg[x][y]

    # plt.figure("src_with_red_cols")
    # plt.imshow(src_with_red_cols)

    # plt.show()
    return threshold_i





