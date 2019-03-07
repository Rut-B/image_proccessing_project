import numpy as np
from pylab import imshow, figure
import matplotlib.pyplot as plt
import cv2
from ex1d import find_line
from ex2c import *
from test3 import *
import scipy.misc

def find_little_rec(src_img):

	h, w = src_img.shape
	first_row = 0
	flag = 0
	# find first row
	for i in range(h):
		if(flag):
			break
		for j in range(w):
			if(src_img[i][j]):
				first_row = i
				flag = 1
				break;
	last_row = h
	flag = 0
	#find last row
	for i in reversed(range(h)):
		if(flag):
			break
		for j in range(w):
			if(src_img[i][j]):
				last_row = i
				flag = 1
				break;

	first_col = 0
	flag = 0
	for i in range(w):
		if(flag):
			break
		for j in range(h):
			if(src_img[j][i]):
				first_col = i
				flag = 1
				break;
	last_col = w
	flag = 0
	for i in reversed(range(w)):
		if(flag):
			break
		for j in range(h):
			if(src_img[j][i]):
				last_col = i
				flag = 1
				break;
	w_newImg = last_col - first_col
	h_newImg = last_row - first_row
	new_img = np.zeros((h_newImg, w_newImg ))

	new_img[0:h_newImg, 0:w_newImg] = src_img[first_row:last_row, first_col:last_col]
	return new_img

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# main
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pathArr = ['8.tif','32.tif','56.tif','63.tif','80.tif']
arrNames= ['8','32','56','63','80']
lastArr = [None] * 5

for i in range(len(pathArr)):
	src_img = cv2.imread(pathArr[i],0)
	src_img_cpy = src_img
	h, w = src_img.shape

	threshold_img = (src_img > 50) * 255
	threshold_img = threshold_img.astype(np.uint8)

	threshold_img_Opp = (src_img > 10) * 255
	threshold_img_Opp = threshold_img_Opp.astype(np.uint8)


	rotated90   = np.rot90(threshold_img_Opp)
	edges       = cv2.Canny(threshold_img,200,255)
	edgesOpp    = cv2.Canny(rotated90,200,255)
	horLines    = find_line(edges)
	verLines    = find_line(edgesOpp)
	verLines    = np.rot90(verLines,3);
	imageBorder = horLines + verLines;
	imageBorder = (imageBorder >= 255)*255
	new_lines   = long_lines(imageBorder)
	mask_img    = fill_rec(new_lines)
	end_img     = np.zeros((h,w))

	for j in range(h):
		for k in range(w):
			if(mask_img[j][k]):
				end_img[j][k] = src_img_cpy[j][k]
			else:
				end_img[j][k]=0
	lastArr[i] = find_little_rec(end_img)

for i in range(len(pathArr)):
	scipy.misc.imsave('output'+ str(arrNames[i])+'.jpg', lastArr[i])
	plt.figure("output image: "+ str(arrNames[i]))
	plt.imshow(lastArr[i] , cmap='gray')
	plt.show()

