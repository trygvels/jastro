
import numpy as np
import matplotlib.pyplot as plt
# from pylab import *
import healpy as hp


fn = 'planck.fits'
map_I = hp.read_map(fn)

# plot the Planck T map
plt.figure()
color = plt.cm.jet
color.set_under("w") # sets background to white
hp.mollview(map_I, title='Planck CMB', unit='mK',norm='hist',cmap=color)
plt.show()

LMAX = 1024
cl = hp.anafast(map_I, lmax=LMAX)
ell = np.arange(len(cl))
plt.figure()
plt.plot(ell, ell * (ell+1) * cl)
plt.xlabel('ell'); plt.ylabel('ell(ell+1)cl'); plt.grid()
plt.show()
