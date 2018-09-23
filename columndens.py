import numpy as np
from healpy import *
import matplotlib.pyplot as plt
import csv
nside = 1024
N = nside2npix(nside) # 12*nside**2
# Reading HI4PI map
path = '/Users/trygveleithesvalheim/datafiles/'
H1map = read_map(path+'data/4PIcolumn.fits')

"""
# Sorting CSV file and constructing map (Not including GLAT AND GLON)
data = np.zeros((N,4))
with open('columndens.csv', 'rb') as f:
    reader = csv.reader(f)
    next(reader, None)
    j = 0
    for row in reader:
        for i in range(4):
            data[j,i] = float(row[i])
        j += 1

data=np.array(sorted(data, key=lambda  l:l[0]))
write_map('4PIcolumn.fits',data[:,3])
"""


# -------- OPTION 1 manual ------------

# Position of polaris flare
lat = np.linspace(23.5,28.5,nside)                    # Latitudal position of polaris flare
lon = np.linspace(121.5,126.5,nside)                 # Longitudal position of polaris flare

polflarePix = np.zeros(nside*nside)
k = 0
for j in range(nside):
    for i in range(nside):
        polflarePix[k] = ang2pix(nside, lon[i], lat[j], lonlat = True) # Find pixel position from angle
        k +=1

# Extracting polaris flare density from H1map
partialdens = np.zeros(N)+UNSEEN                            # Full sky density array
for i in range(len(polflarePix)):
    pixl = int(polflarePix[i])                            # Getting pixel index from ang2pix
    partialdens[pixl] = H1map[pixl]                  # Assigning density values to correct pixels

mollview(partialdens, min=4.7e20, max=9.9e20)
gnomview(partialdens, rot=(124,26),min=4.7e20, max=9.9e20)
plt.show()


# Converting pixel position to angular position (rad)
# !!! not doing anything
#theta, phi = pix2ang(nside, polflarePix)
# Writing fits file with polaris flare density only
#write_map('PD4PI.fits',partialdens,partial=True)
#PDmap = read_map('partialDens.fits')
#mollview(PDmap)

"""
# ----------- OPTION 2 return_projected_map----------
# zooming to middle of polaris flare and extracting data
PFdens = gnomview(H1map,rot=(124,26),return_projected_map = True, title="PF direct from HI4PI")
#plt.savefig('figs/gPF_HI4PI.pdf', bbox_inches='tight',pad_inches=0.106)
plt.show()

# Contrast plot
#plt.hist(PFdens.ravel(), bins=256, range=(0.0, 1.0), fc='k', ec='k')

# Plot extracted data usingn imshow
plt.imshow(PFdens, origin='lower')
plt.title('Polaris flare from HI4PI , 200x200')
plt.xlabel('Pixel #')
plt.ylabel('Pixel #')
plt.colorbar()
#plt.savefig('figs/PF_HI4PI.pdf', bbox_inches='tight',pad_inches=0.106)
plt.show()
"""
"""
# ---- Show full map ----
mollview(H1map, title = 'Full sky map of neutral Hydrogen (HI4PI)',unit='cm^2')
#graticule(coord='G')
#plt.savefig('figs/HI4PI.pdf', bbox_inches='tight',pad_inches=0.106)
plt.show()
"""
