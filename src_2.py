import numpy as np
from pylab import imshow, figure
import matplotlib.pyplot as plt
import cv2
from ex1d import find_line
from ex2c import *
from test3 import *

def filter(img, dimension):
	img_h, img_w = img.shape
	for i in range(img_h - dimension + 1):
		for j in range(img_w - dimension + 1):
			max_value = 0
			for k in range(dimension):
				for l in range(dimension):
					if max_value < img[i + k][j + l]:
						max_value = img[i + k][j + l]
			img[i][j] = max_value
	return img

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
# pathArr  = ['8.tif','32.tif','56.tif','63.tif','80.tif']
pathArr  = ['32.tif']

thrImgArr   		 = [None] * 5
oppThArr    		 = [None] * 5
cannyArr    		 = [None] * 5
cannyOppArr 		 = [None] * 5
linesArr 			 = [None] * 5
linesOppArr 		 = [None] * 5
new_imgArr 			 = [None] * 5
src_with_red_colsArr = [None] * 5
endArr 				 = [None] * 5
lastArr				 = [None] * 5

for i in range(len(pathArr)):
	src_img = cv2.imread(pathArr[i],0)
	src_img_cpy = src_img
	h, w = src_img.shape

	threshold_img = (src_img > 50) * 255
	threshold_img = threshold_img.astype(np.uint8)

	# threshold_img_Opp = (src_img > 10) * 255
	# threshold_img_Opp = threshold_img_Opp.astype(np.uint8)

	plt.figure("threshold_img")
	plt.imshow(threshold_img , cmap='gray')
	plt.show()
	threshold_img = cv2.GaussianBlur(threshold_img,(5,5),0)
	thrImgArr[i]  = threshold_img
	plt.figure("threvvvvshold_img")
	plt.imshow(threshold_img , cmap='gray')
	# plt.show()
	# rotated90     = np.rot90(threshold_img_Opp)
	# oppThArr[i]   = rotated90
	# opp_img = (threshold_img < 255) * 255
	# threshold_img =filter(threshold_img, 3)
	edges    = cv2.Canny(threshold_img,200,255)
	# edgesOpp = cv2.Canny(rotated90,200,255)
	cannyArr[i] = edges
	plt.figure("edges")
	plt.imshow(edges , cmap='gray')
	# plt.show()
	# cannyOppArr[i] = edgesOpp

	# plt.figure("edges")
	# plt.imshow(edges , cmap='gray')

	# plt.figure("edgesOpp")
	# plt.imshow(edgesOpp , cmap='gray')

	# plt.show()
	# linesArr[i] = find_line(edges)
	# linesOppArr[i] = find_line(edgesOpp)
	# linesOppArr[i] = np.rot90(linesOppArr[i],3);
	# new_imgArr[i] = linesArr[i] + linesOppArr[i];
	# new_imgArr[i] = (new_imgArr[i] >= 255)*255
	# minLineLength = 30
	# maxLineGap = 10

	# new_lines = long_lines(new_imgArr[i])

	new_lines = long_lines(edges)
	new_imgArr[i] = new_lines
	# plt.figure("new_lines")
	# plt.imshow(new_lines , cmap='gray')
	plt.figure("new_lines")
	plt.imshow(new_lines , cmap='gray')

	plt.show()
	mask_img = fill_rec(new_lines)
	end_img = np.zeros((h,w))
	for j in range(h):
		for k in range(w):
			if(mask_img[j][k]):
				end_img[j][k] = src_img_cpy[j][k]
			else:
				end_img[j][k]=0
	endArr[i] = end_img
	last_img = find_little_rec(endArr[i])
	lastArr[i] = last_img

for i in range(len(endArr)):
	plt.figure("edges")
	plt.imshow(new_imgArr[i] , cmap='gray')
	plt.figure("canyy")
	plt.imshow(cannyArr[i] , cmap='gray')
	plt.figure("endArr")
	plt.imshow(lastArr[i] , cmap='gray')
# 	plt.figure("src_with_red_colsArr")
# 	plt.imshow(src_with_red_colsArr[i])

	plt.show()

