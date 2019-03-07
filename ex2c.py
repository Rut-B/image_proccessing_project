from tempfile import TemporaryFile
import numpy as np
from pylab import imshow, figure
import matplotlib.pyplot as plt
from copy import copy
import cv2
from canny import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# hough_line - function
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def hough_line(img):
	# Rho and Theta ranges
	thetas = np.deg2rad(np.arange(-90.0, 90.0))
	width, height = img.shape
	diag_len = int(np.ceil(np.sqrt(width * width + height * height)) ) # max_dist
	rhos = np.linspace(-diag_len, diag_len, diag_len * 2.0)
	# Cache some resuable values
	cos_t = np.cos(thetas)
	sin_t = np.sin(thetas)
	num_thetas = len(thetas)
	# Hough accumulator array of theta vs rho
	accumulator = np.zeros((2 * diag_len, num_thetas))
	y_idxs, x_idxs = np.nonzero(img) # (row, col) indexes to edges
	# Vote in the hough accumulator
	for i in range(len(x_idxs)):
		x = x_idxs[i]
		y = y_idxs[i]
		for t_idx in range(num_thetas):
			# Calculate rho. diag_len is added for a positive index
			rho = int( round(x * cos_t[t_idx] + y * sin_t[t_idx]) + diag_len )
			accumulator[rho, t_idx] += 1
	return accumulator, thetas, rhos

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# to_red - function paint red_image
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def to_red(src_img, pattern_img):
	h, w = src_img.shape
	pattern_img_cpy = copy(pattern_img)
	src_img_cpy     = copy(src_img)

	pattern_img_cpy = pattern_img_cpy.astype(np.uint8)
	src_img_cpy = src_img_cpy.astype(np.uint8)

	pattColor  = cv2.cvtColor(pattern_img_cpy, cv2.COLOR_GRAY2RGB)
	srcColor   = cv2.cvtColor(src_img_cpy, cv2.COLOR_GRAY2RGB)


	b,g,r = cv2.split(pattColor)
	g = np.zeros((h, w))
	b = np.zeros((h, w))
	redImg = np.dstack((r,g,b))
	redImg = (redImg).astype(np.uint8)

	src_with_red_cols = srcColor
	for x in range(h):
	    for y in range(w):
	        if(redImg[x][y][0]):
	            src_with_red_cols[x][y] = redImg[x][y]

	return redImg, src_with_red_cols

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# function
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def long_lines(src_img):
	h = len(src_img)
	w = len(src_img[0])

	lines_img     = np.zeros((h, w))
	lines_img_src = np.zeros((h, w))
	end_img       = np.zeros((h, w))

	#hough transform
	accumulator, thetas, rhos = hough_line(src_img)
	accumulator_array = np.array(accumulator).flatten()
	sort_accumulator  = sorted(accumulator_array)

	# find 50 max values
	max_accumulator   = sort_accumulator[-50:]
	max_accumulator   = max_accumulator[::-1]
	max_rho_th = []

	# rho =>[0] theta=>[1]
	max_rho_th.append([0, 0])
	t_threshold = 0.2
	rho_threshold = 50
	status = 0
	mask = np.ones([3,3],np.uint8)
	for i in range(len(max_accumulator)):
		max_val = max_accumulator[i]
		ind_rho, ind_theta = np.nonzero(accumulator == max_val)

		for j in range(0,len(ind_theta)):
			for k in range(1,len(max_rho_th)):
				if((abs(thetas[ind_theta[j]] - max_rho_th[k][1]) <= t_threshold) and (abs(rhos[ind_rho[j]] - max_rho_th[k][0]) <= rho_threshold)):
					status+=1
					break
			if(status == 0):
				max_rho_th.append([rhos[ind_rho[j]], thetas[ind_theta[j]]])
			status = 0

	maxes_array = max_rho_th[1:]

	for i in range(len(maxes_array)):
		cos_t = np.cos(maxes_array[i][1])
		sin_t = np.sin(maxes_array[i][1])
		for ii  in range(len(src_img)):
			for jj in range(len(src_img[0])):
				x = jj*cos_t+ii*sin_t
				if((abs(maxes_array[i][0]-x) <= 1.5)):
				    lines_img[ii][jj] = 255
				    # lines_img_src[ii][jj] = dilate_img[ii][jj]

	lines_img = cv2.dilate(lines_img, mask,iterations = 1)
	return lines_img

if __name__=='__main__':
	main()
