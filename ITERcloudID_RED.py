import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pyfits as pf
import time

path = '/Users/trygveleithesvalheim/datafiles/'
hires = True
start = time.time()


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
    hdulist = pf.open(path+'data/cubesCombinedN.fits')
    N = 933
    MMsheet = 463#464
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

jobs = []

def identifycloud(sheet):
    print "identifying"
    # Sheet 464 has highest mean
    # Getting tolerance and data

    # 1 sigma over mean
    tol = np.mean(reduceddata[MMsheet,:,:]) + 2*np.std(reduceddata[MMsheet,:,:])
    data = reduceddata[sheet,:,:]

    # Making binary array
    clouds = np.where(data>tol)
    for l in range(len(clouds[0])):
            i = clouds[0][l]
            j = clouds[1][l]
            g[i,j] = 1
    #print "g:", g
    print "Binary plot done"
    s = 1
    counter = 0
    for i in range(row):
        for j in range(col):
            if g[i,j]!=0 and w[i,j]==0:
                stepJOB(i,j,s,counter)
                s += 1

    return w,g

def stepJOB(x,y,c,counter):
    cont = True
    while cont == True:
        #counter += 1
        #print counter

        w[x,y] = c # Add data
        cont = False
        for l in range(7):
            if dx[l]==1 and dy[l]==0:
                continue # Avoid adding right step to jobs
            if x>=row-1 or y>=col-1:
                continue # Avoid stepping out of bounds

            nx = x+dx[l] # steps to surrounding points
            ny = y+dy[l]

            # Check surrounding points and add to later jobs
            if g[nx,ny] != 0 and w[nx,ny] == 0 and (nx,ny) not in jobs:
                jobs.append((nx,ny))

        # If stepping right is possible, do it.
        # Else, pick from job list
        if g[x+1,y] != 0 and w[x+1, y] == 0:
            cont = True
            x += 1 # Right step +(1,0)
        elif len(jobs)!=0:
            cont = True
            xy = jobs.pop()
            x = xy[0]
            y = xy[1]
    return

"""
RUN SCRIPT FOR SELECT SHEETS
"""
sheet = 463
print "Working on sheet ", sheet
figr,figrB = identifycloud(sheet=sheet)#MMsheet)
print 'It took', time.time()-start, 'seconds.'
print "plotting"


plt.figure(figsize=(9, 3.5))
plt.subplot(211)
plt.imshow(figrB, cmap = 'spectral', origin="lower")
plt.axis('off')
plt.title('Binary')

# Labelling connected segments

plt.subplot(212)
plt.imshow(figr, cmap= 'spectral', origin="lower")
plt.axis('off')
plt.title('Grouped')

plt.show()
"""
# Sava data!
hdu = pf.PrimaryHDU(figr)
hdulist = pf.HDUList([hdu])
hdulist.writeto(path+'data/idSheets/idS'+str(sheet)+'N.fits', clobber=True)
"""
# Resetting data arrays!
g = np.zeros((row,col))
w = np.zeros((row,col))
jobs = []

print 'It took', time.time()-start, 'seconds to plot and save.'


"""
!! NO DIAGONALS !!
Check indices for a cloud
See if these indices are occupied on next slide
If they are, group these with the previous.
Finally save each cloud separately with their position
Use saved position to get corresponding Density
Save density and position to fits healpix map

"""
# Problem: Naming Conventions
"""
TOMORROW:
Back and forth method.
What about group names?
- If we call first cloud 1, then "cloud 1" exists on all slides
-
Do same as original? 2 arrays (Good idea)
Figure out "already changed"-problem (To save work)
"""
"""
i = 0
while cont = True: # Run untill all clouds are identified

    for sheet in range(20): # Number of sheets
        idx = np.where(data[sheet] == i) # Indices of cloud i

        for j in len(idx):                    # Check each index of cloud
            cloudPixl = data[sheet+1][idx[j]] # data in a point in the cloud on next slide
            if cloudPixl =! 0:                # if next sheet contains cloud in that idx ((AND NOT ALREADY CHANGED))
                grp2change = cloudPixl        # The group on next sheet to be changed
                changeIdx = np.where(data[sheet+1]==grp2change)
                data[sheet+1][changeIdx] = i

    i += 1 # Next cloud
    """
