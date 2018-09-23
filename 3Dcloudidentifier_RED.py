import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pyfits as pf
import sys
sys.setrecursionlimit(100*1000)

"""
Algorithm for cloud identification

# Tolerance for cloud identification
    1 sigma above the average of the middle slide
    print np.mean(reduceddata[46,:,:])
    2.92383

# Check for position of pixels above this average.
    This is a cloud
    Check if cloud continues in z direction

# Identify a cloud by coordinates (Is it connected to other points?
    Take one point, see there are neighboring points

# Check z direction
    Do these clouds have neighboring points on the z axis?
"""

hdulist = pf.open('reducedN.fits')
reduceddata = hdulist[0].data

def levels():
    # Mean densities on all slides
    N = 93
    meanvals = np.zeros(N)
    for i in range(N):
        meanvals[i] = np.mean(reduceddata[i,:,:])
    plt.plot(range(N),meanvals)
    plt.show()
    # Max on slide 46

def histslide(slide):
    # Density histogram on one slide
    plt.hist(reduceddata[slide,:,:].ravel(), bins=256, fc='k', ec='k')
    plt.title('Histogram of densities on slide '+str(slide))
    plt.show()



# Movement around each point
dx = []
dy = []
dz = []
step = [1,-1,0]
for i in step:
    for j in step:
        for k in step:
            if i == 0 and j == 0 and k == 0:
                continue
            dx.append(i)
            dy.append(j)
            dz.append(k)

# Dimension
dep = np.shape(reduceddata)[0]
row = np.shape(reduceddata)[1]
col = np.shape(reduceddata)[2]

# Making binary data
g = np.zeros((dep,row,col))
w = np.zeros((dep,row,col))

def identifycloud():
    # Getting tolerance and data

    tol = np.mean(reduceddata[46,:,:])
    data = reduceddata[:,:,:]

    clouds = np.where(data>tol) # RUNTIME WARNING (BUT CORRECT)

    # Making binary array
    for l in range(len(clouds[0])):
            k = clouds[0][l]
            i = clouds[1][l]
            j = clouds[2][l]
            g[k,i,j] = 1
    #print "g:", g

    # Labeling clouds
    s = 1
    for i in range(row):
        for j in range(col):
            for k in range(dep):
                if g[k,i,j]!=0 and w[k,i,j]==0:
                    dfs(k,i,j,s)      # Identifying  1 cloud
                    s += 1          # Cloud group
    #print "w:",w
    return w,g

def dfs(z, x, y, c):
    # set center value to c
    w[z,x,y] = c

    # set surround values to c if 1
    for i in range(26):
        nx = x+dx[i] # Stepping
        ny = y+dy[i]
        nz = z+dz[i]
        # Avoid walking out of bounds
        if x >= row-1 or y >= col-1 or z>=dep-1:
            continue
        if g[nz,nx,ny] != 0 and w[nz,nx,ny] == 0:
            # RESTART FUNCTION WITH NEW X,Y
            dfs(nz,nx,ny,c)
    return

figr, figrBinary = identifycloud()
hdu = pf.PrimaryHDU(figr)
hdulist = pf.HDUList([hdu])
hdulist.writeto('data/3Didclouds.fits', clobber=True)

sumf = figr.sum(axis=(0))
plt.imshow(figr[45,:,:],origin="lower")
plt.show()
