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

file1= str(sys.argv[1])
unitconv= str(sys.argv[2])
dust1 	 = np.loadtxt(file1)
conv1 	 = np.loadtxt(unitconv, usecols=3)
#gains = np.loadtxt("gains_v15.dat")
band1     = dust1[:,0]
amp1      = dust1[:,1]#/gains
mjyconv =  np.loadtxt(unitconv, usecols=4)
ukRJ1 = (amp1/conv1)


# Create the Modified Blackbody (MBB)
#------------------------------------
h     = 6.626e-34
c     = 3.0e+8
k     = 1.38e-23
nu_ref=857e9
beta  = 1.70
Td    = 19.65
frac_flat = 6.0

x0    = np.empty(2,dtype=float)
x0[0] = beta
x0[1] = Td

bnds  = ((1.0,2.5),(5,50))

x1    = np.empty(3,dtype=float)
x1[0] = beta
x1[1] = Td
x1[2] = frac_flat

bnds1  = ((1.0,2.5), (5,50), (1.0,10.))
x     = np.arange(20,5000,1)
x     = x*1e9

def planck(bet,fre,T):
	return (fre**(bet+1)*(1.0/(np.exp((h*fre)/(k*T))-1)))

def mmbb(beta, T,nu, frac_flat):
        c  = h/(k*T)
        dust = (np.exp(c*nu_ref)-1.) / (np.exp(c*nu)-1.) * (nu/nu_ref)**(beta+1.)* (np.tanh(c*frac_flat*nu)/np.tanh(c*frac_flat*nu_ref))
        return dust
#------------------------------------

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

ukRJ1 = ukRJ1/ukRJ1[0]
#ukRJ2 = ukRJ2/ukRJ2[30]

weights[0]  =  ukRJ1[0]
weights[1]  =  ukRJ1[1]
weights[0]  =  ukRJ1[2]
weights[1]  = (ukRJ1[3]+ukRJ1[4]+ukRJ1[5]+ukRJ1[6]+ukRJ1[7]+ukRJ1[8]+ukRJ1[9]+ukRJ1[10])/8
weights[2]  = (ukRJ1[12]+ukRJ1[13]+ukRJ1[14]+ukRJ1[15]+ukRJ1[16]+ukRJ1[17]+ukRJ1[18]+ukRJ1[19]+ukRJ1[20]+ukRJ1[21])/10
weights[3]  = (ukRJ1[22]+ukRJ1[23]+ukRJ1[24]+ukRJ1[25]+ukRJ1[26]+ukRJ1[27]+ukRJ1[28]+ukRJ1[29])/8
weights[4]  = (ukRJ1[30]+ukRJ1[31]+ukRJ1[32])/3
weights[5]  = (ukRJ1[33])
# Minimize the Planck fit with scipy.minimize
#--------------------------------------------
Bv = planck(beta,x,Td)

chisq = 0.0

def fit(x):
	chisq = 0.0
	for i in range(len(weights)):
		model = planck(x[0],freqs[i]*1e9,x[1])/planck(x[0],nu_ref,x[1])

		chisq = chisq + (weights[i] - model)**2#/weights[i]**2
	# model = planck(x[0],freq[34]*1e9,x[1])/planck(x[0],857*1e9,x[1])
	# chisq = chisq + (ukRJ[34] - model)**2
	return chisq

result    = minimize(fit,x0,bounds=bnds)

z         = np.empty(2,dtype=float)
z[0],z[1] = result.x

z[0] = round(z[0],3)
z[1] = round(z[1],3)
#print(z)

# Minimize mmbb
#--------------------------------------------
chisq = 0.0

def fit(x):
        chisq = 0.0
        for i in range(len(weights)):
                model = mmbb(x[0],x[1], freqs[i]*1e9,x[2])
                chisq = chisq + (weights[i] - model)**2#/weights[i]**2
        return chisq

result    = minimize(fit,x1,bounds=bnds1)

z1         = np.empty(3,dtype=float)
z1[0],z1[1], z1[2] = result.x

z1[0] = round(z1[0],4)
z1[1] = round(z1[1],4)
z1[2] = round(z1[2],4)
#print(z)

#--------------------------------------------

# The minimized MBB fit
#--------------------------------------------
Bv = planck(z[0],x,z[1])

Bv = Bv/(planck(z[0],nu_ref,z[1]))

x = x*1e-9

#print(Bv)

#--------------------------------------------
plt.figure(figsize=(10, 8))
ymax=2.0
ymin=0.01 #np.min(ukRJ)
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


plt.scatter(freq,ukRJ1, label=file1, marker="o", color="C0")

data = np.loadtxt("daniel.dat")
plt.scatter(data[:,0],data[:,1], label="Daniel", marker="o", color="C1")

spec = r'$\beta$ = ' + str(z[0])
tem = r'$T_d$ = ' + str(z[1])
plt.plot(x,Bv,label=r'MBB '+spec+", "+tem+" fitted", color="C3")

spec = r'$\beta$ = ' + str(z1[0])
tem = r'$T_d$ = ' + str(z1[1])
d = r'$d$ = ' + str(z1[2])
plt.plot(x,mmbb(z1[0],z1[1],x*1e9,z1[2]),label=r'MMBB '+spec+", "+tem+", "+d+ " fitted", color="C0")

         
beta=1.6
temp=17.4
spec = r'$\beta$ = ' + str(beta)
tem = r'$T_d$ = ' + str(temp)
scale = 1.0#0.787
plt.plot(x,(mmbb(beta, temp, x*1e9, 6.0)/mmbb(beta,temp, nu_ref, 6.0))*scale,label=r'MMBB '+spec +", "+tem+" from commander",color='black', linestyle='--', alpha=0.5)

beta=1.62
temp=19.7
spec = r'$\beta$ = ' + str(beta)
tem = r'$T_d$ = ' + str(temp)
scale = 1.0#0.891
plt.plot(x,(planck(beta, x*1e9, temp)/planck(beta, nu_ref, temp))*scale,label=r'MBB '+spec +", "+tem+" planck 2015",color='black', linestyle=':', alpha=0.5)


#plt.text(185,0.5,spec)#,size=20)
#plt.text(185,0.4,tem)#,size=20)
plt.legend(loc=4)
plt.title('857 Dust Template Fitting')
plt.xticks()
plt.yticks()
plt.ylim(ymin,ymax)
plt.xlim(10,1000)
plt.xlabel('Freq (GHz)')
plt.ylabel(r'Amplitude ($uK_{RJ}$)')
plt.yscale('log')
plt.xscale('log')
plt.tight_layout()
plt.savefig('dusttemp.png')
plt.show()
