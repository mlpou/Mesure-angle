import matplotlib.pyplot as plt # type: ignore
import numpy as np # type: ignore
from sklearn.linear_model import LinearRegression # type: ignore
from sklearn.preprocessing import PolynomialFeatures # type: ignore
import os
import matplotlib.pyplot as plt # type: ignore
import astropy # type: ignore
import astropy.convolution as apconv # type: ignore
from pathlib import Path

path = "D:\\data\\172.20.4.160\\A"


def centre_de_masse(images):
	R=images[:,:,0]
	G=images[:,:,1]
	B=images[:,:,2]
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
	max = np.max(image2)
	return [resultx, resultY, max]

def numberToAlt (number,altIterations, altPrecision, azIteration) : 
    # On retourne l'angle selon le nombre dans l'itération
    angle = (((number//azIteration)-altIterations/2)*altPrecision)
    return angle

L= []
for entry in os.listdir(path) : 
     imageTmp=entry
     if entry != "regression.txt" :  
         image=plt.imread(entry)
         mot = ""
         for l in range(4) :
             if ord(entry[l+21]) >= 48 and ord(entry[l+21]) <=57 :
                 mot = mot + entry[l+21]
         i = int(mot)
         ListeTemp = centre_de_masse(image) + [i]
         if ListeTemp[2] > 50 :
             L.append(ListeTemp)


expx = []
expy = []
expz = []
theoz = []

for i in range(len(L)) : 
    expx[i] = L[i][0]
    expy[i] = L[i][1]
    expz[i] = numberToAlt(L[i][3])
    theoz[i] = -17.0103 + 2.1920*10^(-2)*expx[i] + 1.7805*10^(-5)*expx[i]^2 - 1.5477*10^(-8)*expx[i]^3 + 2.4758*10^(-12)*expx[i]^4 - 6.4732*10^(-4)*expy[i] + 5.7307*10^(-5)*expy[i]^2 - 6.0212*10^(-8)*expy[i]**3 + 1.5105*10^(-11)*expy[i]^4


plt.plot(expx, expy, expz, label="exp")
plt.plot(expx, expy, theoz, label = "theo")




