import numpy as np
import healpy as hp
import pyfits as pf
import matplotlib.pyplot as plt
from skimage import data, filters, measure, exposure
from skimage.filters import threshold_mean
import time
start = time.time()
path = '/Users/trygveleithesvalheim/datafiles/data/'
c1 = 420 # Sheets with data
c2 = 475


def combcubes(savefits,plotsum, hemis, speedup):
    #Combine data cubes for northern and southern hemisphere

    if hemis=="N": # Choosing hemishphere
        CAR1 = "CAR_A"
        CAR2 = "CAR_B"
    else:
        CAR1 = "CAR_H"
        CAR2 = "CAR_I"

    for i in range(1,19): # 1 to 18

        # String for readfile
        if i < 10:
            numb = str(0)+str(i)
        else:
            numb = str(i)


        # Removing overlap horizontally (Right side removal)
        hdulist = pf.open(path+CAR1+str(numb)+'.fits') # First row
        Hs = hdulist[0].data
        hdulist.close()

        if speedup==True:
            Hs=Hs[c1:c2,:,:]

        Hs = np.delete(Hs, np.s_[240:], axis = 2) # Correcting for overlap in X

        hdulist = pf.open(path+CAR2+str(numb)+'.fits') # Second Row
        Is = hdulist[0].data
        hdulist.close()

        if speedup==True:
            Is=Is[c1:c2,:,:]

        Is = np.delete(Is, np.s_[240:], axis = 2) # Correcting for overlap in X

        # Where are we
        print hemis,numb

        # Combining data cubes horizontically
        if i>1:
            Hdata = np.concatenate((Hs,Hdata),axis=2)
            Idata = np.concatenate((Is,Idata),axis=2)
        else:
            Hdata = Hs
            Idata = Is

        # Check shape of data array
        print np.shape(Hdata)

    # Correcting for overlap in Y
    if hemis=="N":
        print "Deleting extra on N"
        Idata = np.delete(Idata, np.s_[240:], axis = 1) # FOR NORTH
        Hdata = np.delete(Hdata, np.s_[240:], axis = 1) # FOR NORTH
    else:
        print "Deleting extra on S"
        Idata = np.delete(Idata, np.s_[:26], axis = 1)
        Hdata = np.delete(Hdata, np.s_[:26], axis = 1)
    # Combining data cubes vertically
    data = np.concatenate((Hdata,Idata), axis=1)

    # Freeing up memory
    Hdata = []
    Idata = []
    Hs = []
    Is = []

    # Check shape of data array
    print np.shape(data)

    # Saving to fits file
    if savefits == True:
        print "saving"
        hdu = pf.PrimaryHDU(data)
        hdulist = pf.HDUList([hdu])
        hdulist.writeto(path+'cubesCombined'+str(hemis)+'.fits',clobber=True)

    if plotsum == True:
        sumpf = data.sum(axis=(0))
        plt.imshow(sumpf,origin='lower')
        plt.title(hemis+'hemisphere overlap corrected')
        plt.xlabel('Galactic longitude')
        plt.ylabel('Galactic latitude')
        plt.savefig('figs/cubesComb'+hemis+'.png', bbox_inches='tight',pad_inches=0.106)
        plt.show()
    return data

dataN = combcubes(savefits=False, plotsum=False, hemis="N", speedup=True)
dataS = combcubes(savefits=False, plotsum=False, hemis="S", speedup=True)


###########################
######## Cloud ID #########
###########################
thresh = 4. # From slide 446 mean+sigma for northern hemisphere

def cloudID(c1,c2, plot, data):
    data = data[c1,c2]                # Use only selected sheets
    clouds = data                     # Select slides
    # Binary image
    binary = clouds > thresh          # Create binary image of data above threshold
    # Labelling connected segments
    clouds_grouped = measure.label(binary, background=0)    # Segment clouds in 3D data
    numberofclouds = np.max(clouds_grouped) # Find highest number assigned to cloud
    print "Number of identified clouds: ", numberofclouds

    LOSclouds = np.zeros((numberofclouds,480,4320)) #CHANGE TO 2160

    for ID in range(1,numberofclouds+1): # Number of clouds when using 1 sigma threshold in range 420:475
        singleCloud = clouds_grouped == ID                  # Show only one cloud

        idx = np.where(singleCloud>0)       # Index of cloud
        w = np.zeros(np.shape(singleCloud)) # With density data
        w[idx] = data[idx]        # Extract densities
        sumw = w.sum(axis=(0))    # LOS integration over 1 cloud
        LOSclouds[ID-1] = sumw
        print ID

    return clouds_grouped, LOSclouds

z = np.zeros((np.shape(dataN)[0],1680, 4320)) # Extra array for full sky array
alldata = np.concatenate((dataN,z), axis=1)
alldata = np.concatenate((alldata,dataS), axis=1)

sumc = alldata.sum(axis=(0))
plt.imshow(sumc, cmap = 'nipy_spectral', origin="lower")
plt.show()

all_clouds, LOSclouds = cloudID(c1,c2, plot=False, data=alldata)

"""
# Northern hemisphere clouds
all_clouds, LOSclouds = cloudID(c1,c2, plot=False, data=dataN)

#hdu = pf.PrimaryHDU(LOSclouds)
#hdulist = pf.HDUList([hdu])
#hdulist.writeto(path+'data/LOScloudsN.fits',clobber=True)


# Southern hemisphere clouds
all_clouds, LOSclouds = cloudID(c1,c2, plot=False, data=dataS)

hdu = pf.PrimaryHDU(LOSclouds)
hdulist = pf.HDUList([hdu])
hdulist.writeto(path+'data/LOScloudsS.fits',clobber=True)

print 'It took', time.time()-start, 'seconds.'
"""

sumc = all_clouds.sum(axis=(0))
plt.imshow(sumc, cmap = 'nipy_spectral', origin="lower")
plt.show()

plt.imshow(LOSclouds,cmap = 'nipy_spectral', origin="lower")
plt.show()


#######################################
######## Convert to mollweide #########
#######################################
nside = 512
npix = 12*nside**2

hdulist = pf.open(path+'data/LOScloudsN.fits')
LOScloudsN = hdulist[0].data
hdulist = pf.open(path+'data/LOScloudsS.fits')
LOScloudsS = hdulist[0].data
