import numpy as np
from healpy import *
import matplotlib.pyplot as plt
import csv
N = 609

data = np.zeros((9,N))
with open('result.csv', 'rb') as f:
    reader = csv.reader(f)
    next(reader, None)
    j = 0
    for row in reader:
        for i in range(9):
            data[i,j] = float(row[i])
        j += 1
pd = np.zeros(N) #Debiased polarization array
for i in range(N):
    pd[i] = np.sqrt(data[4,i]**2-data[5,i]**2)

gEVPA = data[8,:] #EVPA - Polarization angle array

# Making lines and centering on star
startx = np.zeros(N+1)
starty = np.zeros(N+1)
endx = np.zeros(N+1)
endy = np.zeros(N+1)
k = 10. #Scaling length
for i in range(N):
    endx[i] = data[2,i]+pd[i]/2*np.sin(gEVPA[i]*np.pi/180.)/k
    endy[i] = data[3,i]+pd[i]/2*np.cos(gEVPA[i]*np.pi/180.)/k
    startx[i] = endx[i]-pd[i]*np.sin(gEVPA[i]*np.pi/180.)/k
    starty[i] = endy[i]-pd[i]*np.cos(gEVPA[i]*np.pi/180.)/k

#Annotation for scale
startx[N] = 121
endx[N] = 121+(1./k)
starty[N] = 28
endy[N] = 28
plt.annotate('1%',
    xy=(121.1, 28.05))


plt.plot([startx,endx],[starty,endy], ms=0.2, color="red")

#plt.plot(data[2,:],data[3,:],'o', ms=0.8)
plt.xlabel('Galactic Longitude [Degrees]')
plt.ylabel('Galactic Latitude [Degrees]')
plt.gca().invert_xaxis()
plt.show()


"""
Length of each segment is proportional to debiased p
pd = np.sqrt(p**2-sp**2)

Orientation of each line:
EVPA

Position of each line:
data 2 and 3


Write pd = 1

"""
