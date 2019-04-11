import matplotlib as mpl
import sys
#mpl.rcParams.update(mpl.rcParamsDefault)
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
plt.style.use(u"trygveplot")
#mpl.rcParams['text.usetex'] = True


#dust1 	 = np.loadtxt('dust_amplitudes_v12.dat')
#conv1 	 = np.loadtxt('unit_conversions_v12.dat', usecols=3)

#band1     = dust1[:,0]
#amp1      = dust1[:,1]

#ukRJ2 = amp1/conv1
version = str(sys.argv[1])

dust = "dust_amplitudes_ame1_"+version+".dat"
ff = "ff_amplitudes_"+version+".dat"
synch = "synch_amplitudes_"+version+".dat"
unitconv= "unit_conversions_"+version+".dat"
dust1 	 = np.loadtxt(dust)
synch1 	 = np.loadtxt(synch)
ff1 	 = np.loadtxt(ff)
conv1 	 = np.loadtxt(unitconv, usecols=3)

dust1 = (dust1[:,1]/conv1)
dust1 = dust1/dust1[33]

synch1 = (synch1[:,1]/conv1)
synch1 = synch1/synch1[0]

ff1 = (ff1[:,1]/conv1)
ff1 = ff1/ff1[0]



band_range1  = np.empty(2)
band_range2  = np.empty(2)
band_range3  = np.empty(2)
band_range4  = np.empty(2)
band_range5  = np.empty(2)
band_range6  = np.empty(2)
band_range7  = np.empty(2)
band_range8  = np.empty(2)
band_range9  = np.empty(2)
band_range10 = np.empty(2)
band_range11 = np.empty(2)
band_range12 = np.empty(2)
band_range13 = np.empty(2)
band_range14 = np.empty(2)
band_range15 = np.empty(2)
band_range16 = np.empty(2)
band_range17 = np.empty(2)

#band_range1  = [1000,1540]   # DIRBE 1250
#band_range2  = [1780,2500]	# DIRBE 2140
#band_range3  = [2600,3500]	# DIRBE 3000
band_range4  = [23.9,34.5]	# Planck 30
band_range5  = [39,50]		# Planck 44
band_range6  = [60,78]		# Planck 70
band_range7  = [82,120]		# Planck 100
band_range8  = [125,170]	# Planck 143
band_range9  = [180,265]	# Planck 217
band_range10 = [300,430]	# Planck 353
band_range11 = [450,650]	# Planck 545
band_range12 = [700,1020]	# Planck 857
band_range13 = [30,37]		# WMAP Ka
band_range14 = [21,25.5]	# WMAP K
band_range15 = [38,45]		# WMAP Q
band_range16 = [54,68]		# WMAP V
band_range17 = [84,106]		# WMAP W

freq = np.empty(48)
freq = [30,44,70,100,100,100,100,100,100,100,100,143,217,217,217,217,217,217,217,217,217,217,353,353,353,353,353,353,353,353,545,545,545,857,857,857,857,0.4,22.8,33,40.6,40.6,60.8,60.8,93.5,93.5,93.5,93.5]#,1250,2140,3000]

weights     = np.empty(6)
freqs       = np.empty(8)

freqs[0]  = 30
freqs[1]  = 44
freqs[0]  = 70
freqs[1]  = 100
freqs[2]  = 217
freqs[3]  = 353
freqs[4]  = 545
freqs[5]  = 857


#ukRJ2 = ukRJ2/ukRJ2[30]
#--------------------------------------------
plt.figure()#figsize=(10, 8))
ymax=2.0
ymin=0.01 #np.min(ff1)#0.0001 #np.min(ukRJ)
# plt.text(22.8,0.00055,"K",size=20,color='#006600')
# plt.text(31.5,0.00055,"Ka",size=20,color='#006600')
# plt.text(39.,0.00055,"Q",size=20,color='#006600')
# plt.text(58.,0.00055,"V",size=20,color='#006600')
# plt.text(90.,0.00055,"W",size=20,color='#006600')

plt.text(27,ymax-0.2,"30",color='black', va='top',alpha=0.5)
plt.text(42,ymax-0.2,"44",color='black', va='top',alpha=0.5)
plt.text(64,ymax-0.2,"70",color='black', va='top',alpha=0.5)
plt.text(90,ymax-0.2,"100",color='black', va='top',alpha=0.5)
plt.text(135,ymax-0.2,"143",color='black', va='top',alpha=0.5)
plt.text(200,ymax-0.2,"217",color='black', va='top',alpha=0.5)
plt.text(330,ymax-0.2,"353",color='black', va='top',alpha=0.5)
plt.text(490,ymax-0.2,"545",color='black', va='top',alpha=0.5)
plt.text(770,ymax-0.2,"857",color='black', va='top',alpha=0.5)
#plt.text(1100,ymax-0-2,r"240$\mu$m",size=15,color='#CC0000', va='top')
#plt.text(1800,ymax-0-2,r"140$\mu$m",size=15,color='#CC0000', va='top')
#plt.text(2700,ymax-0-2,r"100$\mu$m",size=15,color='#CC0000', va='top')
#plt.axvspan(band_range1[0],band_range1[1],color='red',hatch='+',alpha=0.3,label='DIRBE')
#plt.axvspan(band_range2[0],band_range2[1],color='red',hatch='+',alpha=0.3)
#plt.axvspan(band_range3[0],band_range3[1],color='red',hatch='+',alpha=0.3)
plt.axvspan(band_range4[0],band_range4[1],color='C2',hatch='//',alpha=0.3)
plt.axvspan(band_range5[0],band_range5[1],color='C2',hatch='//',alpha=0.3)
plt.axvspan(band_range6[0],band_range6[1],color='C2',hatch='//',alpha=0.3)
plt.axvspan(band_range7[0],band_range7[1],color='C2',hatch='//',alpha=0.3)
plt.axvspan(band_range8[0],band_range8[1],color='C2',hatch='//',alpha=0.3)
plt.axvspan(band_range9[0],band_range9[1],color='C2',hatch='//',alpha=0.3)
plt.axvspan(band_range10[0],band_range10[1],color='C2',hatch='//',alpha=0.3)
plt.axvspan(band_range11[0],band_range11[1],color='C2',hatch='//',alpha=0.3)
plt.axvspan(band_range12[0],band_range12[1],color='C2',hatch='//',alpha=0.3)
# plt.axvspan(band_range13[0],band_range13[1],color='green',hatch='\\',alpha=0.3)
# plt.axvspan(band_range14[0],band_range14[1],color='green',hatch='\\\\',alpha=0.5,label='WMAP')
# plt.axvspan(band_range15[0],band_range15[1],color='green',hatch='\\\\',alpha=0.5)
# plt.axvspan(band_range16[0],band_range16[1],color='green',hatch='\\\\',alpha=0.5)
# plt.axvspan(band_range17[0],band_range17[1],color='green',hatch='\\\\',alpha=0.5)


plt.scatter(freq,dust1, label=dust, marker="o", color="C0")
plt.scatter(freq,synch1, label=synch, marker="o", color="C1")
plt.scatter(freq,ff1, label=ff, marker="o", color="C2")


#plt.text(185,0.5,spec)#,size=20)
#plt.text(185,0.4,tem)#,size=20)
plt.legend(loc=4)
plt.title('Fullsky template fitting on '+version)
plt.xticks()
plt.yticks()
plt.ylim(ymin,ymax)
plt.xlim(10,1000)
plt.xlabel('Freq (GHz)')
plt.ylabel(r'Amplitude ($uK_{RJ}$)')
plt.yscale('log')
plt.xscale('log')
plt.tight_layout()
plt.savefig('fullfit_big_'+version+'.png')
plt.show()
