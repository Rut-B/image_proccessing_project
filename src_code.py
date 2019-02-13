import numpy as np
from pylab import imshow, figure
import matplotlib.pyplot as plt
import cv2
from ex1d import find_line
from ex2c import *
from test3 import *
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# main
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# pathArr  = ['8.tif','32.tif','56.tif','63.tif','80.tif']


plt.show()
thrImgArr = [None] * 5
oppThArr = [None] * 5
cannyArr = [None] * 5
cannyOppArr = [None] * 5
linesArr = [None] * 5
linesOppArr = [None] * 5
new_imgArr = [None] * 5
src_with_red_colsArr = [None] * 5

pathArr  = ['8.tif']
for i in range(len(pathArr)):
	src_img = cv2.imread(pathArr[i],0)
	h, w = src_img.shape
	threshold_img = (src_img > 50) * 255
	threshold_img = threshold_img.astype(np.uint8)

	threshold_img_Opp = (src_img > 10) * 255
	threshold_img_Opp = threshold_img_Opp.astype(np.uint8)
	# plt.figure("threshold_img_Opp")
	# plt.imshow(threshold_img_Opp, cmap = 'gray')

	thrImgArr[i]  = threshold_img
	rotated90=np.rot90(threshold_img_Opp)
	oppThArr[i]=rotated90
	opp_img = (threshold_img < 255) * 255
	edges    = cv2.Canny(threshold_img,200,255)
	edgesOpp = cv2.Canny(rotated90,200,255)
	cannyArr[i] = edges
	cannyOppArr[i] = edgesOpp

	# plt.figure("edgesOpp")
	# plt.imshow(edgesOpp, cmap = 'gray')

	linesArr[i] = find_line(edges)
	linesOppArr[i] = find_line(edgesOpp)
	linesOppArr[i] = np.rot90(linesOppArr[i],3);
	new_imgArr[i] = linesArr[i] + linesOppArr[i];
	new_imgArr[i] = (new_imgArr[i] >= 255)*255
	# plt.figure("liness")
	# plt.imshow(new_img ,cmap = 'gray')
	# plt.show()
	minLineLength = 30
	maxLineGap = 10
	# new_imgArr[i] =new_imgArr[i].astype(np.float32)
	# data = np.array(new_imgArr[i], dtype=np.float32)
	# print(type(data[0][0]))
	# lines = cv2.HoughLinesP(data,1,np.pi/180,15,minLineLength,maxLineGap)
	# for x in range(0, len(lines)):
	#     for x1,y1,x2,y2 in lines[x]:
	#         cv2.line(src_img,(x1,y1),(x2,y2),(0,255,0),2)
	# plt.figure("cv2cv2cv2")
	# plt.imshow(src_img )
	# plt.show()
	new_lines = long_lines(new_imgArr[i])
	fill_rec(new_lines)
	np.savetxt('text.txt',new_lines,fmt='%.2f')
	# plt.figure("long_lines")
	# plt.imshow(new_lines ,cmap = 'gray')
	redImg, src_with_red_cols = to_red(src_img, new_lines)
	src_with_red_colsArr[i] = src_with_red_cols
	# plt.figure("redImg")
	# plt.imshow(redImg )
	# plt.figure("src_with_red_cols")
	# plt.imshow(src_with_red_cols )
	# plt.show()
# 	sumArr = [sum(x) for x in zip(*linesArr[i])]
# 	print(sumArr)
# 	max_value = max(sumArr)
# 	max_index = sumArr.index(max_value)

# 	print(max_value)
# 	print(max_index)

for i in range(len(linesArr)):
	# plt.figure("liness")
	# plt.imshow(linesArr[i] ,cmap = 'gray')
	# plt.figure("liness22")
	# plt.imshow(linesOppArr[i] ,cmap = 'gray')
	plt.figure("new_imgArr")
	plt.imshow(new_imgArr[i] )
	plt.figure("src_with_red_colsArr")
	plt.imshow(src_with_red_colsArr[i])

	plt.show()

# for i in range(len(pathArr)):
# 	src_img = cv2.imread(pathArr[i],0)
# 	h, w = src_img.shape
# 	threshold_img = (src_img > 70) * 255
# 	threshold_img = threshold_img.astype(np.uint8)
# 	thrImgArr[i] = threshold_img
# 	plt.figure("threshold_img"+str(i))
# 	plt.imshow(threshold_img, cmap = 'gray')

# 	rotated90=np.rot90(threshold_img)
# 	plt.figure("ffff")
# 	plt.imshow(rotated90, cmap = 'gray')
# 	oppThArr[i]=rotated90
# 	opp_img = (threshold_img < 255) * 255
# 	plt.figure("opp_img")
# 	plt.imshow(opp_img, cmap = 'gray')



# 	edges = cv2.Canny(threshold_img,200,255)

# 	plt.subplot(121)
# 	plt.imshow(threshold_img,cmap = 'gray')
# 	plt.title('Original Image')
# 	plt.xticks([]), plt.yticks([])
# 	plt.subplot(122)
# 	plt.imshow(edges,cmap = 'gray')
# 	plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

# 	# plt.show()
# 	find_line(edges)
# 	plt.show()
