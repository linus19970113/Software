import cv2
import numpy as np
import argparse, sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import Counter
from sklearn.cluster import KMeans
from sklearn import linear_model
import IPython
import time

NUM_COLORS = 3

CENTERS = np.array([[0, 0, 0], [0, 255, 255], [255, 255, 255]])
# print CENTERS 

np.random.seed(5)

IMG_PATH = '''IMG PATH'''

#cv_img = cv2.imread("test2.jpg")
# print cv_img.shape

# class GetKMeansModel(object):
# 	def __init__(self, img)
def getimgdatapts(cv2img):

	x, y, p = cv2img.shape
	cv2_tpose=cv2img.transpose()
	cv2_arr_tpose=np.reshape(cv2_tpose,[p,x*y])
	npdata=np.transpose(cv2_arr_tpose);

	return npdata

#priors
def runKMeans(cv_img):
	testdata = getimgdatapts(cv_img)
	kmc = KMeans(n_clusters = NUM_COLORS, max_iter = 100, n_init = 10, init = CENTERS)
	kmc.fit_predict(imgdata)
	trained_centers = kmc.cluster_centers_
	print trained_centers
	# print CENTERS
	labels = kmc.labels_
	labelcount = Counter()
	for pixel in labels:
		labelcount[pixel] += 1
	print labelcount
	return trained_centers, labelcount


def identifyColors(trained, true):
	# print trained
	# print np.size(trained)
	numcolors, _ = np.shape(trained)
	# print numcolors
	matching = np.zeros((numcolors, numcolors))
	# print matching
	for i, color in enumerate(trained):
		# print color
		for j, truecolor in enumerate(true):
			matching[i][j] = np.linalg.norm(color - truecolor)

	print matching
	colormap= {}
	for i, color in enumerate(matching):
		colormap[i] = np.argmin(color)
		# colormap[2] = 1
		print colormap
	colormap = checkMapping(colormap)
	return colormap

def checkMapping(mymap):
	maplist = []
	clearmap = {}
	for color, mapping in mymap.iteritems():
		if mapping not in maplist:
			clearmap[color] = mapping
			maplist += mapping
	print clearmap
	return clearmap


def getparameters(mapping, trained, true):
	redX = np.zeros((3, 1))
	redY = np.zeros((3, 1))
	greenX = np.zeros((3, 1))
	greenY = np.zeros((3, 1))
	blueX = np.zeros((3, 1))
	blueY = np.zeros((3, 1))
	# print type(redY), redX
	print trained, true
	for i, color in enumerate(true):
		mapped = mapping[i]
		# print i, color
		for j, index in enumerate(color):
			# print index, j
			if j == 0:
				redY[i] = index
			if j == 1:
				greenY[i] = index
			if j == 2:
				blueY[i] = index
		for j2, index2 in enumerate(trained[mapped]):

			if j2 == 0:
				# print redX
				redX[i] = index2
				# print redX
			if j2 == 1:
				greenX[i] = index2
			if j2 == 2:
				blueX[i] = index2
	# print redX
	print redX, redY
	RED = linear_model.LinearRegression()
	BLUE = linear_model.LinearRegression()
	GREEN = linear_model.LinearRegression()
	RED.fit(redX, redY)
	BLUE.fit(blueX, blueY)
	GREEN.fit(greenX, greenY)
	print RED.coef_, RED.intercept_
	print BLUE.coef_, BLUE.intercept_
	print GREEN.coef_, GREEN.intercept_
	return (RED.coef_, RED.intercept_), (BLUE.coef_, BLUE.intercept_), (GREEN.coef_, GREEN.intercept_)

def scaleandshift(img,scale,shift):
	h = img.shape[0]
	w = img.shape[1]

	img_scale = np.reshape(img,[h*w,3])
	img_scale = np.reshape(img_scale*np.array(scale),[h,w,3])

	img_shift = np.reshape(img_scale,[h*w,3])
	img_shift = np.reshape(img_shift+np.array(shift),[h,w,3])

	return img_shift

if __name__ == '__main__':
	img_filename="test2.jpg"
	if (len(sys.argv)>1):
		img_filename=sys.argv[1]
		print(img_filename)
	cv_img = cv2.imread(img_filename)
	t1=time.clock();
	testdata = getimgdatapts(cv_img)
	t2=time.clock();
	print("Time taken:")
	print(t2-t1)
	
	trained = runKMeans(testdata)
	mapping = identifyColors(trained[0], CENTERS)
	getparameters(mapping, trained[0], CENTERS)