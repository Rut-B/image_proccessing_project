from matplotlib import pyplot as plt
import cv2
import numpy as np
from copy import copy
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# main - functions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def fill_rec(src_img):

    h, w = src_img.shape
    mask = np.ones([5,5],np.uint8)

    output_img = np.zeros((h,w))
    output_img[int(h/2)][int(w/2)] = 255
    oppsite_img = (src_img < 255)*255

    #Region filling
    for iter_ in range(220):
        dilation_cntrs = cv2.dilate(output_img.astype(np.uint8), mask, iterations=1)
        for i in range(h):
            for j in range(w):
                if oppsite_img[i][j]!= dilation_cntrs[i][j]:
                    output_img[i][j] = 0
                else:
                    output_img[i][j]=dilation_cntrs[i][j]

    return output_img
if __name__=='__main__':
    main()
