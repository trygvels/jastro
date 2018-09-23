
import sys
import numpy as np
import healpy as hp
import pyfits as pf
import matplotlib.pyplot as plt
from skimage import data, filters, measure, exposure, morphology
from skimage.filters import threshold_mean
import time
nside = 512
npix = 12*nside**2
hpmap = np.zeros(hp.nside2npix(nside), dtype=np.double)

numclouds = 25
for i in range(numclouds):
    hdulist = pf.open('clouds2/cloud'+str(i)+'.fits') # First row
    cld = hdulist[0].data

    binary = cld > 0
    hpmap+=binary

hp.mollview(hpmap)
plt.show()
