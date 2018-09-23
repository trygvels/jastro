import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pyfits as pf


"""
Data CUBE!
20x20x933
We have a pixel range of 120-140 long and 10-30 lat

Each image spans 20x20 degrees
each pixel in each image is 0.08333333330000001 degrees

130 lon is pixel number 136.5 where N = 271
20 lat is pixel number 134.6 where N = 275

!!!! PF:
lon (126.5-121.5)
lat (23.5 - 28.5)
pfdata = zoom(126.5,121.5,28.5,23.5)
"""
hdulist = pf.open('TAN_F07.fits')

def printheader():
    #print data header
    print hdulist[0].header
    return

# Extract and plot data 933 arrays of len 275
HIdata = hdulist[0].data

def zoom(x1,x2,y1,y2):
    # Calculating pixel position of PF
    d = 0.08333333330000001
    dx1 = (x1-130)/d
    dx2 = (x2-130)/d
    dy1 = (y1-20)/d
    dy2 = (y2-20)/d


    xx1 = int(275-round(136.5+dx1)) # Pixel value at 121.5
    xx2 = int(275-round(136.5+dx2)) # Pixel value at 126.5

    yy1 = int(round(134.6460+dy1)) # Pixel value at 23.5
    yy2 = int(round(134.6460+dy2)) # Pixel value at 28.5
    pfdata = HIdata[:,xx1:xx2,yy2:yy1] # Extracting PF data
    return pfdata

pfdata = zoom(126.5,121.5,28.5,23.5) # !PF
#pfdata = zoom(126,125,27,26) # PF portion

def plotLOS(save):
    # LoS integration on cube
    sumpf = pfdata.sum(axis=(0))/933.
    plt.imshow(sumpf,origin='lower')
    plt.colorbar()
    plt.title('LoS Integration PF cube')
    if save == True:
        plt.savefig('figs/sumCube.pdf', bbox_inches='tight',pad_inches=0.106)
    plt.show()
    return

def plotslices(save):
    # Slices of data cube
    fig, axarr = plt.subplots(4, 4)
    fig.suptitle("4x4 slices of PF 20x20 density cube", fontsize=16)
    clim = (np.min(pfdata[520]),np.max(pfdata[464]))
    subplots = 18
    for i,v in enumerate(xrange(subplots)):
        nbr = 450+v
        v = v+1
        ax1 = plt.subplot(3,6,v)
        ax1.imshow(pfdata[nbr],origin='lower',clim=clim)
        ax1.set_title(str(nbr))
        plt.axis('off')
    fig.tight_layout()
    if save == True:
        plt.savefig('figs/cubeSlices.pdf', bbox_inches='tight',pad_inches=0.106)
    plt.show()
    return


def plot3Dcube(tol,show,save):
    #3D scatter plot of cube with tolerance as argument
    x = np.arange(np.shape(pfdata)[1])
    y = np.arange(np.shape(pfdata)[2])
    z = list(reversed(np.arange(np.shape(pfdata)[0]))) # TO FLIP
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for k in z:
        for i in x:
            for j in y:
                if pfdata[k,i,j]>tol:
                    p = ax.scatter(x[i],y[j],z[k],c=pfdata[k,i,j],cmap='jet',vmin=6,vmax=37)
                    ax.set_zlim3d(455,495)
    fig.colorbar(p)
    plt.xlim(-5,65)
    plt.ylim(-5,65)
    plt.title('PF cube, densities larger than: '+str(tol))
    if save == True:
        plt.savefig('figs/slideshow/tol'+str(tol)+'.pdf', bbox_inches='tight',pad_inches=0.106)
        plt.close()
    if show == True:
        plt.show()
    return

for i in range(6,37):
    plot3Dcube(float(i), False, True)
