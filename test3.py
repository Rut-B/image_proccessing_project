from matplotlib import pyplot as plt
import cv2
import numpy as np
from copy import copy
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# main - functions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def fill_rec(src_img):

    h, w = src_img.shape
    mask = np.ones([11,11],np.uint8)
    np.set_printoptions(threshold=np.nan)

    output_img = np.zeros((h,w))
    output_img[int(h/2)][int(w/2)] = 100

    #Region filling
    for iter_ in range(220):
        dilation_cntrs = cv2.dilate(output_img.astype(np.uint8), mask, iterations=1)
        # print(dilation_cntrs);
        np.savetxt('textrrr.txt',dilation_cntrs,fmt='%.2f')
    #     break;
    #     for i in range(h):
    #         for j in range(w):
    #             if oppsite_img[i][j]!= dilation_cntrs[i][j]:
    #                 output_img[i][j] = 0
    #             else:
    #                 output_img[i][j]=dilation_cntrs[i][j]

    # output_img = (output_img < 50) * 255

    # plt.figure("ricde countrs - input")
    # plt.imshow(dilation_cntrs_cpy, cmap='gray')

    # rice_filling = output_img + dilation_cntrs_cpy
    # rice_filling_add = (rice_filling >=255)*255

    # plt.figure("final rice filling - output ")
    # plt.imshow(rice_filling_add , cmap='gray')
    # plt.show()

if __name__=='__main__':
    main()
