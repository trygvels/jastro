from skimage import data, filters, measure, exposure
from skimage.filters import threshold_mean
from skimage.transform import resize
import matplotlib.pyplot as plt
import pyfits as pf
import numpy as np
import healpy as hp

path = '/Users/trygveleithesvalheim/datafiles/'
#image_array = resize(LOScloudsN,(NY,NX)) # Resizing image

hdulist = pf.open(path+'data/LOScloudsN.fits')
LOScloudsN = hdulist[0].data
hdulist = pf.open(path+'data/LOScloudsS.fits')
LOScloudsS = hdulist[0].data

south = True
NN = 338 # Identified clouds in N. hemisphere
NS = 438 # Identified clouds in S. hemisphere
N = NN+NS
nside = 512
npix = 12*nside**2
z = np.zeros((1680, 4320)) # Extra array for full sky array

if south == True: # Need to do north and south separate bc memory
    all_clouds = np.zeros((NS,2160,4320))
    for i in range(NS):
        all_clouds[i] = np.concatenate((LOScloudsS[i],z), axis=0)
else:
    all_clouds = np.zeros((NN,2160,4320))
    for i in range(NN):
        all_clouds[i] = np.concatenate((z,LOScloudsN[i]), axis=0)

"""
Converting to healpix map
"""
# Find theta and phi coordinates of image
theta = np.linspace(0, np.pi, num = 2160)[:, None]
phi = np.linspace(-np.pi, np.pi, num = 4320)

# Get pixel positions of full picture
pix = hp.ang2pix(nside, theta, phi)

for i in range(np.shape(all_clouds)[0]):
    # Reset healpix map array
    healpix_map = np.zeros(hp.nside2npix(nside), dtype=np.double)

    # put image in healpy map array
    healpix_map[pix] = all_clouds[i] # Magic

    if np.shape(np.where(healpix_map > 0))[1] < 1:
        print "Cloud " + str(NS+i) + " was empty with length:" + str(np.shape(np.where(healpix_map>0))[1])
        continue

    else:

        healpix_map[np.where(healpix_map == 0)] = hp.UNSEEN # Set empty pixels to UNSEEN

        healpix_map = healpix_map[::-1]
        """
        hp.mollview(healpix_map, title="Clouds number: " + str(i))
        plt.show()
        """
        hp.write_map(path+'data/cloudsFITS/cloud'+str(NS+i)+'.fits',healpix_map, partial=True)
