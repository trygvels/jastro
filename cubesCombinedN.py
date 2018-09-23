import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pyfits as pf
path = '/Users/trygveleithesvalheim/datafiles/'

"""
For the northern hemisphere we combine all H1:18 and I1:18 cubes.
Use Concatenate function
"""
def combcubes(savefits,plotsum):
    for i in range(1,19):

        # String for readfile
        if i < 10:
            numb = str(0)+str(i)
        else:
            numb = str(i)

        # Reading files
        hdulist = pf.open(path+'data/CAR_A'+str(numb)+'.fits')
        Hs = hdulist[0].data
        Hs = np.delete(Hs, np.s_[:26], axis = 1) # Correcting for overlap
        #Hs = np.delete(Hs, np.s_[240:], axis = 1) # Correcting for overlap # FOR NORTH
        Hs = np.delete(Hs, np.s_[240:], axis = 2) # Correcting for overlap
        hdulist.close()

        hdulist = pf.open(path+'data/CAR_B'+str(numb)+'.fits')
        Is = hdulist[0].data
        Is = np.delete(Is, np.s_[:26], axis = 1) # Correcting for overlap
        #Is = np.delete(Is, np.s_[240:], axis = 1) # Correcting for overlap # FOR NORTH
        Is = np.delete(Is, np.s_[240:], axis = 2) # Correcting for overlap
        hdulist.close()

        # Where are we
        print numb

        # Combining data cubes horizontically
        if i>1:
            Hdata = np.concatenate((Hs,Hdata),axis=2)
            Idata = np.concatenate((Is,Idata),axis=2)
        else:
            Hdata = Hs
            Idata = Is

        # Check shape of data array
        print np.shape(Hdata)

    # Combining data cubes vertically
    data = np.concatenate((Hdata,Idata), axis=1)

    # Check shape of data array
    print np.shape(data)

    # Saving to fits file
    if savefits == True:
        print "saving"
        hdu = pf.PrimaryHDU(data)
        hdulist = pf.HDUList([hdu])
        hdulist.writeto(path+'data/cubesCombinedS.fits',clobber=True)

    if plotsum == True:
        sumpf = data.sum(axis=(0))/933.
        plt.imshow(sumpf,origin='lower')
        plt.title('Southern hemisphere overlap corrected')
        plt.xlabel('Galactic longitude')
        plt.ylabel('Galactic latitude')
        plt.savefig('figs/cubesCombS.png', bbox_inches='tight',pad_inches=0.106)
        plt.show()
    return data


# Calling function
data = combcubes(savefits=True, plotsum=False)
print "plotting"
plt.imshow(data[464], cmap='nipy_spectral',origin="lower")
plt.show()

"""
REDUCING DATA
"""
def reduce(scale, savefits, plotsum):
    hdulist = pf.open(path+'data/cubesCombinedN.fits')
    data = hdulist[0].data

    # Reducing data with scale factor
    from sklearn.feature_extraction.image import extract_patches

    patches = extract_patches(data, patch_shape=(scale, scale, scale), extraction_step=(scale,scale,scale))
    reduceddata = patches.mean(-1).mean(-1).mean(-1)

    # Print shape of new data
    print np.shape(reduceddata)

    # Plot LOS if requested
    if plotsum == True:
        print "Summing data"
        sumpf = reduceddata.sum(axis=(0))/93.
        print "Plotting data"
        plt.imshow(sumpf,origin='lower')
        plt.show()

    # Save to fits if requested
    if savefits == True:
        hdu = pf.PrimaryHDU(reduceddata)
        hdulist = pf.HDUList([hdu])
        hdulist.writeto('data/reducedN.fits')

    return reduceddata

#reduceddata = reduce(10, True, True)





"""
Cubes overlap.
Check factor of overlapping by comparing one sheet to another.

QUESTION:
Why does the header say third value is radio velocity?
Why is the data so flat?
Why is the new fits file so small?
How deep is the z direction in physical units?
"""

##############
#OVERLAP CHECK
# Overlap visible when comparing H01 and H02 on sheet 465
# Approximately 26 pixels overlap, Crop on RHS and bottom of all H?
#############
"""
hdulist = pf.open('data/CAR_H01.fits')
Sheet1 = hdulist[0].data
print hdulist[0].header
hdulist.close()
plt.hist(Sheet1[400:550,:,:].ravel(), bins=256, fc='k', ec='k')
plt.show()

meanvals = np.zeros(150)
for i in range(400,550):
    meanvals[i-400] = np.mean(Sheet1[i,:,:])
print np.mean(Sheet1[440:480,:,:])
plt.plot(range(400,550),meanvals)
plt.show()
"""
"""
hdulist = pf.open('data/CAR_H01.fits')
Sheet1 = hdulist[0].data
Sheet1 = np.delete(Sheet1, np.s_[240:], axis = 1)
Sheet1 = np.delete(Sheet1, np.s_[240:], axis = 2)
print np.shape(Sheet1)
hdulist.close()

hdulist = pf.open('data/CAR_H02.fits')
Sheet2 = hdulist[0].data
Sheet2 = np.delete(Sheet2, np.s_[240:], axis = 1)
Sheet2 = np.delete(Sheet2, np.s_[240:], axis = 2)
hdulist.close()

hdulist.close()
hdulist = pf.open('data/CAR_I01.fits')
Sheet3 = hdulist[0].data
Sheet3 = np.delete(Sheet3, np.s_[240:], axis = 1)
Sheet3 = np.delete(Sheet3, np.s_[240:], axis = 2)
hdulist.close()

hdulist.close()
hdulist = pf.open('data/CAR_I02.fits')
Sheet4 = hdulist[0].data
Sheet4 = np.delete(Sheet4, np.s_[240:], axis = 1)
Sheet4 = np.delete(Sheet4, np.s_[240:], axis = 2)
hdulist.close()

nbr = 465
plt.subplot(2,2,1)
plt.imshow(Sheet2[nbr,:,:], vmin=np.min(Sheet2[nbr,:,:]), vmax=np.max(Sheet2[nbr,:,:]))

plt.subplot(2,2,2)
plt.imshow(Sheet1[nbr,:,:], vmin=np.min(Sheet2[nbr,:,:]), vmax=np.max(Sheet2[nbr,:,:]))

plt.subplot(2,2,3)
plt.imshow(Sheet4[nbr,:,:], vmin=np.min(Sheet2[nbr,:,:]), vmax=np.max(Sheet2[nbr,:,:]))

plt.subplot(2,2,4)
plt.imshow(Sheet3[nbr,:,:], vmin=np.min(Sheet2[nbr,:,:]), vmax=np.max(Sheet2[nbr,:,:]))


plt.subplots_adjust(wspace=0, hspace=0)


plt.show()
"""
