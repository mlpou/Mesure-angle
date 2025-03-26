import numpy as np # type: ignore
import os
import matplotlib.pyplot as plt # type: ignore
import astropy # type: ignore
import astropy.convolution as apconv # type: ignore
from pathlib import Path

path = "/home/Mesure-angle/dossier_test_image"

L=[]
def convolve(imag, window):
	return apconv.convolve(imag, apconv.Box2DKernel(width=window))
    
def centre_de_masse(images):
	R=image[:,:,0]
	G=image[:,:,1]
	B=image[:,:,2]
	image2=R/3+B/3+G/3
	image2[image2 < 40] = 0
	arr=image2
	rows=arr.shape[0]
	cols=arr.shape[1]
	arr_y=arr*np.arange(1,rows+1).reshape(-1,1)
	arr_x=arr*np.arange(1,cols+1).reshape(1,-1)
	num_y=np.sum(arr_y)
	denom_y=np.sum(arr)
	num_x=np.sum(arr_x)
	denom_x=np.sum(arr)
	resultY=num_y/denom_y
	resultx=num_x/denom_x
	return [resultx, resultY]

i = 0

os.chdir(path)
for entry in os.listdir(path):
	imageTmp=entry
	image=plt.imread(entry)
	ListeTemp=centre_de_masse(image)+[i]
	L.append(ListeTemp)
	i += 1



print(centre_de_masse(path))