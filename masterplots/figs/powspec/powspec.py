from matplotlib import rcParams, rc
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.interpolate

dir = "/Users/trygveleithesvalheim/Documents/jobb/jastro/masterplots/figs/powspec/"
plt.style.use(u"trygveplot")

params = {'savefig.dpi': 300, # save figures to 300 dpi
          'ytick.major.size' : 0,
          'ytick.minor.size' : 0,
          'xtick.major.size' : 0,
          'xtick.minor.size' : 0,

          'axes.grid.axis' : 'y',
          'axes.grid' : True
          }
rcParams.update(params)

pell, pcl, perrup, perrdo = np.loadtxt("planck_CL.txt", unpack=True)
lell, lcl, lerrup, lerrdo, lol, lal = np.loadtxt("cl_LCDM.txt", unpack=True)

pell_hi, lmin,lmax, pcl_hi, pclerr = np.loadtxt("planck_CL_hil.txt", unpack=True)

well, wellmin, wellmax, wcl, werr,wmerr,wcerr=np.loadtxt("wmap_CL_bin.txt", unpack=True)


plt.errorbar(pell, pcl,yerr=[perrdo,perrup], fmt='.',color="C0", label="Planck")
plt.errorbar(pell_hi,pcl_hi,yerr=pclerr, fmt='.',color="C0")
plt.errorbar(well, wcl, yerr=wmerr,fmt='.',color="C1",label="WMAP")
plt.errorbar(lell, lcl, color="C7", label=r"Best fit $\Lambda CDM$", alpha=0.5)
plt.ylabel(r"$l(l+1)C_l/2\pi$")
plt.xlabel("Multipole moment, l")
plt.legend()
plt.xlim(0,1500)
plt.ylim(0,6000)
plt.savefig(dir+"powspec.pdf", bbox_inches='tight',  pad_inches=0.02)
plt.show()
