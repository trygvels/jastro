import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pyfits as pf
hires = False

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

# Hires or lores data
if hires==True:
    hdulist = pf.open('/Users/trygveleithesvalheim/datafiles/data/cubesCombinedN.fits')
    N = 933  # BEWARE THIS IS NOT PIXEL PRECICION
    MMsheet = 464
else:
    hdulist = pf.open('reducedN.fits')
    N = 93
    MMsheet = 46

reduceddata = hdulist[0].data

def levels():
    # Mean densities on all slides
    meanvals = np.zeros(N)
    for i in range(N):
        meanvals[i] = np.mean(reduceddata[i,:,:])

    plt.plot(range(N),meanvals)
    plt.show()

def histslide(slide):
    std = np.std(reduceddata[slide,:,:])
    print 'STD:', std
    print 'Mean+1',  np.mean(reduceddata[slide,:,:])+std
    print 'Mean+2',  np.mean(reduceddata[slide,:,:])+2*std
    # Density histogram on one slide
    plt.hist(reduceddata[slide,:,:].ravel(), bins=256, fc='k', ec='k')
    plt.title('Histogram of densities on slide '+str(slide))
    plt.show()


# Movement around each point
dx = [-1,0,1,1,1,0,-1,-1]
dy = [1,1,1,0,-1,-1,-1,0]
# Dimension
row = np.shape(reduceddata)[1]
col = np.shape(reduceddata)[2]
# Making binary data
g = np.zeros((row,col))
w = np.zeros((row,col))

import sys
sys.setrecursionlimit(50000)

def identifycloud(sheet):
    print "identifying"
    # Sheet 464 has highest mean
    # Getting tolerance and data

    tol = np.mean(reduceddata[MMsheet,:,:]) + 2*np.std(reduceddata[MMsheet,:,:])
    print tol
    data = reduceddata[sheet,:,:]
    clouds = np.where(data>tol)
    #print clouds

    # Making binary array
    for l in range(len(clouds[0])):
            i = clouds[0][l]
            j = clouds[1][l]
            g[i,j] = 1
    #print "g:", g
    print "Binary plot done"

    # Labeling clouds
    s = 1
    for i in range(row):
        for j in range(col):
            if g[i,j]!=0 and w[i,j]==0:
                step(i,j,s)      # Identifying 1 cloud
                s += 1          # Cloud group
    return w,g

def step(x,y,c):
    # set center value to c
    w[x,y] = c

    # set surround values to c if 1
    for l in range(8):
        nx = x+dx[l] # Stepping
        ny = y+dy[l]

        if g[nx,ny] != 0 and w[nx,ny] == 0:
            # RESTART FUNCTION WITH NEW X,Y, and continue this
            step(nx,ny,c)
    return

figr,figrB = identifycloud(sheet=MMsheet)
print "plotting"
plt.imshow(figr,origin="lower")
plt.show()
"""
hdu = pf.PrimaryHDU(figr)
hdulist = pf.HDUList([hdu])
hdulist.writeto('../datafiles/data/idclouds.fits', clobber=True)
"""
