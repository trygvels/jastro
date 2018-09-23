from skimage import data, filters, measure, exposure
from skimage.filters import threshold_mean
import healpy as hp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pyfits as pf
import time
import numpy as np

start = time.time()
path = '/Users/trygveleithesvalheim/datafiles/'
hdulist = pf.open(path+'data/cubesCombinedN.fits')
data = hdulist[0].data

# Density threshold
MMsheet = 464
#thresh = np.mean(data[MMsheet]) + 2*np.std(data[MMsheet])
c1 = 420
c2 = 475
print np.mean(data[c1:c2]) + 2*np.std(data[c1:c2])
print np.mean(data[c1:c2]) + 1*np.std(data[c1:c2])
print np.mean(data[c1:c2])
# Prev 7.79615
# tresh2 = 5.
# tresh3 = 4.
thresh = 4. # From slide 446 mean+sigma for northern hemisphere

def plotsheet(clouds_grouped, singleCloud, slide, cloudid):
    plt.figure(figsize=(9, 2.5))
    plt.subplot(211)
    plt.imshow(clouds_grouped, cmap = 'nipy_spectral', origin="lower")
    plt.axis('off')
    plt.title('Grouped, Threshold '+str(thresh)+" Slide: "+str(slide))

    plt.subplot(212)
    plt.imshow(singleCloud, cmap= 'nipy_spectral', origin="lower")
    plt.axis('off')
    plt.title('Single cloud. ID:' + str(cloudid))

    plt.show()


def cloudID(c1,c2, plot):
    clouds = data                     # Select slides
    # Binary image
    binary = clouds > thresh          # Create binary image of data above threshold
    # Labelling connected segments
    clouds_grouped = measure.label(binary, background=0)    # Segment clouds in 3D data
    numberofclouds = np.max(clouds_grouped)
    print "Number of identified clouds: ", numberofclouds

    LOSclouds = np.zeros((numberofclouds,480,4320))

    for ID in range(1,numberofclouds+1): # Number of clouds when using 1 sigma threshold in range 420:475
        singleCloud = clouds_grouped == ID                  # Show only one cloud
        for i in range(np.shape(clouds_grouped)[0]):            # Iterate over every sheet
            if plot==True:
                plotsheet(clouds_grouped[i],singleCloud[i],c1+i,ID) # Plotting

        idx = np.where(singleCloud>0)       # Index of cloud
        w = np.zeros(np.shape(singleCloud)) # With density data
        w[idx] = data[idx]        # Extract densities
        sumw = w.sum(axis=(0))    # LOS integration over 1 cloud
        LOSclouds[ID-1] = sumw
        print ID
        # For finding cloud ID
        #print clouds_grouped[i][0,4000] #135 for 420:475

    return clouds_grouped, LOSclouds

"""
EXTRACTING DENSITY data
beware ID's not constant when changing sheet range. STICK TO 420:475
"""
c1 = 420
c2 = 475
data = data[c1:c2]
all_clouds, LOSclouds = cloudID(c1,c2, plot = False)


print 'It took', time.time()-start, 'seconds.'

hdu = pf.PrimaryHDU(LOSclouds)
hdulist = pf.HDUList([hdu])
hdulist.writeto(path+'data/LOScloudsN.fits',clobber=True)





# Sum plot
sumc = all_clouds.sum(axis=(0))
plt.imshow(sumc, cmap = 'nipy_spectral', origin="lower")
plt.show()
