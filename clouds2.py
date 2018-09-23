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

"""
def combcubes(hemis):
    #Combine data cubes for northern and southern hemisphere
    print "combining cubes"
    print "concatenating horizontally"
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
        Hs=Hs[c1:c2,:,:]

        Hs = np.delete(Hs, np.s_[240:], axis = 2) # Correcting for overlap in X
        hdulist.close()

        hdulist = pf.open(path+CAR2+str(numb)+'.fits') # Second Row
        Is = hdulist[0].data
        Is=Is[c1:c2,:,:]

        Is = np.delete(Is, np.s_[240:], axis = 2) # Correcting for overlap in X
        hdulist.close()

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
        #print np.shape(Hdata)

    # Correcting for overlap in Y
    if hemis=="N":
        Idata = np.delete(Idata, np.s_[240:], axis = 1) # FOR NORTH
        Hdata = np.delete(Hdata, np.s_[240:], axis = 1) # FOR NORTH
    else:
        Idata = np.delete(Idata, np.s_[:26], axis = 1)
        Hdata = np.delete(Hdata, np.s_[:26], axis = 1)
    # Combining data cubes vertically
    data = np.concatenate((Hdata,Idata), axis=1)

    # Freeing up memory
    Hdata = None
    Idata = None
    Hs = None
    Is = None

    # Check shape of data array
    #print np.shape(data)
    print "concatenating vertically"
    return data

dataN = combcubes(hemis="N")
dataS = combcubes(hemis="S")
print "constructing full image"
alldata = np.zeros((np.shape(dataN)[0],1200, 4320)) # Extra array for full sky array
alldata = np.concatenate((dataN,alldata), axis=1) #Concatenate and overwrite
alldata = np.concatenate((alldata,dataS), axis=1)
hdu = pf.PrimaryHDU(alldata)
hdulist = pf.HDUList([hdu])
hdulist.writeto(path+'allsky.fits',clobber=True)
print "Saved"
"""

print "opening data"
hdulist = pf.open(path+'allsky.fits') # First row
alldata = hdulist[0].data

###########################
######## Cloud ID #########
###########################
thresh = 35. # 4 Take a better look at this
            # 7 works with memory?
def cloudID(data):
    print "identifying clouds"
    #data = data[c1,c2]                # Use only selected sheets
    clouds = data                     # Select slides
    # Binary image
    binary = clouds > thresh          # Create binary image of data above threshold
    # Labelling connected segments
    clouds_grouped = measure.label(binary, background=0)    # Segment clouds in 3D data
    numberofclouds = np.max(clouds_grouped) # Find highest number assigned to cloud
    print "Number of identified clouds: ", numberofclouds

    LOSclouds = np.zeros((numberofclouds,2160,4320))

    for ID in range(1,numberofclouds+1): # Number of clouds when using 1 sigma threshold in range 420:475
        singleCloud = clouds_grouped == ID                  # Show only one cloud
        idx = np.where(singleCloud>0)       # Index of cloud

        w = np.zeros(np.shape(singleCloud)) # With density data
        w[idx] = data[idx]        # Extract densities
        LOSclouds[ID-1] = w.sum(axis=(0))    # LOS integration over 1 cloud
        print ID

    return LOSclouds


"""
sumc = alldata.sum(axis=(0))
plt.imshow(sumc, cmap = 'nipy_spectral', origin="lower")
plt.show()
"""

LOSclouds = cloudID(data=alldata)
all_clouds = LOSclouds
LOSclouds = None #Free up memory

#######################################
######## Convert to mollweide #########
#######################################
print "converting to mollweide"
nside = 512
npix = 12*nside**2

# Find theta and phi coordinates of image
theta = np.linspace(0, np.pi, num = 2160)[:, None]
phi = np.linspace(-np.pi, np.pi, num = 4320)

# Get pixel positions of full picture
pix = hp.ang2pix(nside, theta, phi)

i = 0
j = 0
while j<np.shape(all_clouds)[0]:
    # Reset healpix map array
    healpix_map = np.zeros(hp.nside2npix(nside), dtype=np.double)

    # put image in healpy map array
    healpix_map[pix] = all_clouds[i] # Magic

    if np.shape(np.where(healpix_map > 0))[1] < 5:
        print "Cloud " + str(i) + " was empty with length:" + str(np.shape(np.where(healpix_map>0))[1])
        j+=1
        continue

    else:
        healpix_map[np.where(healpix_map == 0)] = hp.UNSEEN # Set empty pixels to UNSEEN

        healpix_map = healpix_map[::-1]

        hp.mollview(healpix_map, title="Clouds number: " + str(i))
        plt.show()
        print "writing cloud number ", i, " to file"
        hp.write_map(path+'clouds2/cloud'+str(i)+'.fits',healpix_map, partial=True)
        i += 1
        j += 1

print "number of clouds after reduction:", i
print "reduced to ", float(i)/float(j)*100, " percent"
print "time elapsed: ", (time.time()-start)/60./60., ' hours.'
print "cloud identification done"
