from skimage import data, filters, measure, exposure
from skimage.filters import threshold_mean
from skimage.transform import resize
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pyfits as pf
import time
import numpy as np
import healpy as hp
from healpy.projector import CartesianProj
from healpy.projector import MollweideProj
# benjamin.racine@astro.uio.no
start = time.time()
path = '/Users/trygveleithesvalheim/datafiles/'


# MAX SLIDES ON N: 134 (ID:135) and 136 (ID:137)
# MAX SLIDES ON S: 6 (ID:7)
# Data: 360 degrees longitude, 50-90 latitude
# Dimensions: (480,4320)
# Full map: (2160,4320) need to add 1680

NN = 338 # Identified clouds in N. hemisphere
NS = 438 # Identified clouds in S. hemisphere
nside = 512
npix = 12*nside**2
z = np.zeros((1680, 4320)) # Extra array for full sky array

"""
full
"""
c1 = 420
c2 = 475
hdulist = pf.open(path+'data/cubesCombinedN.fits')
Nfull = hdulist[0].data
hdulist = pf.open(path+'data/cubesCombinedS.fits')
Sfull = hdulist[0].data

fullLOSN = Nfull[c1:c2].sum(axis=(0))
fullLOSS = Sfull[c1:c2].sum(axis=(0))

# Add empty array for converting to full sky
fullLOSS = np.concatenate((fullLOSS, z), axis=0)
fullLOSN = np.concatenate((z,fullLOSN), axis=0)

full = fullLOSN + fullLOSS
"""
Add full first
"""
hdulist = pf.open(path+'data/LOScloudsN.fits')
LOScloudsN = hdulist[0].data
hdulist = pf.open(path+'data/LOScloudsS.fits')
LOScloudsS = hdulist[0].data

# LOS of all clouds
LOScloudsN = LOScloudsN.sum(axis=(0))
LOScloudsS = LOScloudsS.sum(axis=(0))

# Add empty array for converting to full sky
LOScloudsS = np.concatenate((LOScloudsS, z), axis=0)
LOScloudsN = np.concatenate((z,LOScloudsN), axis=0)

# Add N and S hemisphere
image_array = LOScloudsN+LOScloudsS

"""
GENERAL
"""
# Find theta and phi coordinates of image
theta = np.linspace(0, np.pi, num=image_array.shape[0])[:, None]
phi = np.linspace(-np.pi, np.pi, num=image_array.shape[1])

# Get pixel positions of full picture
pix = hp.ang2pix(nside, theta, phi)

"""
GENERAL END
"""
# Make healpix map array
healpix_map = np.zeros(hp.nside2npix(nside), dtype=np.double)

# put image in healpy map array
healpix_map[pix] = image_array # Magic
#healpix_map[np.where(healpix_map == 0)] = hp.UNSEEN # Set empty pixels to UNSEEN

"""
For full
"""
full_map = np.zeros(hp.nside2npix(nside), dtype=np.double)

full_map[pix] = full # Magic
#full_map[np.where(healpix_map == 0)] = hp.UNSEEN # Set empty pixels to UNSEEN

"""
Full end
"""
le = full_map - healpix_map
ma = le[::-1]
ma[np.where(ma == 0)] = hp.UNSEEN

full_map[np.where(full_map == 0)] = hp.UNSEEN
fu = full_map[::-1]
healpix_map[np.where(healpix_map == 0)] = hp.UNSEEN
se = healpix_map[::-1]

"""
hp.write_map(path+'data/fullHI50.fits',fu, partial=True)
hp.write_map(path+'data/segmentedHI50.fits',se, partial=True)
hp.write_map(path+'data/cloudsFITS/subtractedHI50fits',ma, partial=True)
"""
#min = 4.
#max = 350.
hp.mollview(fu,title="Full map +50 GLAT",sub=311)
hp.mollview(se,title="Above threshold (4.0) +50 GLAT", sub = 312)
hp.mollview(ma,title="Diff +50 GLAT",sub=313)
plt.savefig('figs/diff4a.pdf', bbox_inches='tight',pad_inches=0.106)
plt.show()

"""
NX = 4320
NY = 2160
#image_array = resize(LOScloudsN,(NY,NX)) # Resizing image
"""
