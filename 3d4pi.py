import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pyfits as pf

hdulist = pf.open('data/MOL.fits')

def printheader():
    #print data header
    print hdulist[0].header
    return

cube4pi = hdulist[0].data
print np.shape(cube4pi)
sheets = []

tol = np.nanmean(cube4pi[440:480,:,:]) # 8 from 440:480
# Degrading data 10fold

print tol

def plot3Dcube(tol,show,save,sheet):
    print sheet
    #3D scatter plot of cube with tolerance as argument
    x = np.arange(np.shape(cube4pi)[2])
    y = np.arange(np.shape(cube4pi)[1])
    #z = list(reversed(np.arange(15)))#np.shape(cube4pi)[2]))) # FLIP

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #for k in z:
    for i in x:
        for j in y:
            if cube4pi[sheet,j,i]>tol:
                p = ax.scatter(i,sheet,j,c=cube4pi[sheet,j,i],cmap='jet',vmin=tol,vmax=140)
                ax.set_zlim3d(-50,2000)
                save = True
    #fig.colorbar(p)
    print save
    plt.xlim(-50,4000)
    plt.ylim(-10,960)
    plt.title('Full sky cube, sheet: '+str(sheet))
    if show == True:
        plt.show()
    if save == True:
        sheets.append(sheet)
        plt.savefig('figs/3d4pi_slide/TOL'+str(tol)+'S'+str(sheet)+'.png', bbox_inches='tight',pad_inches=0.106)
    plt.close()
    return
#for i in range(362,945):
#    plot3Dcube(50,False,False,i)

#print sheets

def reducedata(tol):
    x = np.arange(np.shape(cube4pi)[2])
    y = np.arange(np.shape(cube4pi)[1])
    z = np.arange(np.shape(cube4pi)[0])
    data = np.zeros(np.shape(cube4pi)[2],np.shape(cube4pi)[1],np.shape(cube4pi)[0])
    for i in x:
        for j in y:
            for k in z:
                if cube4pi[k,j,i] > tol:
                    data[i,j,k] = cube4pi[k,j,i]
    """
    Write data to file

    """
    return

"""
Alternative: Make data arrays beforehand, filter them, and then plot.

#
Go through all data and note z-slides within tolerance

Tolerance should be the same as in PF.. 6?

##
Problems with this method:
Picture too small, cant tell clouds apart. Dots too big.
All clouds too close together

Potential Fix
Make picture a lot bigger, and plot everything at the same time.

###
Use imshow??? Maybe turn down resolution?
How to do this in 3d?

####
Turn down resolution?
"""
