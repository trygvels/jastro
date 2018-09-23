from matplotlib import rcParams, rc
import matplotlib.pyplot as plt
import numpy as np
import math
dir = "/Users/trygveleithesvalheim/Documents/jobb/jastro/masterplots/figs/spec_param/"
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

h    = 6.62607e-34 # Planck's konstant
k_b  = 1.38065e-23 # Boltzmanns konstant
Tcmb = 2.7255      # K CMB Temperature
def cmb(nu, A):
    x = h*nu/(k_b*Tcmb)
    g = (np.exp(x)-1)**2/(x**2*np.exp(x))
    s_cmb = A/g
    return s_cmb

def sync(nu, As, alpha):
    #alpha = 1., As = 30 K (30*1e6 muK)
    nu_0 = 0.408*1e9 # 408 MHz
    fnu, f = np.loadtxt(dir+"Synchrotron_template_GHz_extended.txt", unpack=True)
    f = np.interp(nu, fnu*1e9, f)
    f0 = np.interp(nu_0, nu, f) # Value of s at nu_0

    s_s = As*(nu_0/nu)**2*f/f0
    return s_s


def ff(nu,EM,Te):
    #EM = 1 cm-3pc, Te= 500 #K
    T4 = Te/1e4
    nu9 = nu/1e9 #Hz
    g_ff = np.log(np.exp(5.960-np.sqrt(3)/np.pi*np.log(nu9*T4**(-3./2.)))+np.e)
    tau = 0.05468*Te**(-3./2.)*nu9**(-2)*EM*g_ff
    s_ff = 1e6*Te*(1-np.exp(-tau))
    return s_ff


def sdust(nu, Asd, nup):
    #s_sd = Asd*(nu0/nu)**2*(fsd(nu*nup0/nup)/fsd(nu0*nup0/nup))
    #nup0=30.0*1e9
    nu_0 = 41.e9 #nu10=22.8*1e9, nu20=41.0*1e9
    fnu, f = np.loadtxt(dir+"spdust2_cnm.dat", unpack=True)
    # (nup0/nup) = 30./31. = 1.
    f = np.interp(nu, fnu*1e9, f)
    f0 = np.interp(nu_0, nu, f) # Value of s at nu_0
    s_sd = Asd*(nu_0/nu)**2*f/f0
    return s_sd

def tdust(nu,Ad,betad,Td):
    nu0=545.*1e9
    gamma = h/(k_b*Td)
    s_d=Ad*(nu/nu0)**(betad+1)*(np.exp(gamma*nu0)-1)/(np.exp(gamma*nu)-1)
    return s_d

def lf(nu,Alf,betalf):
    return Alf*(nu)**(betalf)

"""
N = 1000


nu = np.linspace(0,1000,N)
CMB = cmb(nu*1e9,70)
LFn = lf(nu,1e6,-3.0)
LF = lf(nu,1e6,-3.1)

FF = ff(nu*1e9, 100., 7000.)
SYNC = sync(nu*1e9,30.*1e6,1.)
SDUST = sdust(nu*1e9,100.,11.*1e9)

TDUST = tdust(nu*1e9,100,1.53,20.1)
TDUSTn = tdust(nu*1e9,100,1.6,23.)
sumf = LF+TDUST
fgs=[CMB,LF,TDUST,LFn,TDUSTn]
col=["C9","C0","C2","C1","C3","C4","C7"]
label=["CMB","Thermal Dust", "Low-freq.","Thermal Dust", "Low-freq.","Sum fg."]
rot=[-2, -35, -45, -70, 27, -45]
idx=[15, 150, 120, 80, 20, 50]
yidx=[0, 150, 150, 100, 300, 30]
scale=[7,2.3,180]
j=0
for i in range(len(fgs)):
    plt.loglog(nu,fgs[i], linewidth=4,color=col[i])
    if i==0 or i==4:
        plt.text(nu[idx[i]], fgs[i][idx[i]]+scale[j], label[i], rotation=rot[i], color=col[i],fontsize=12)
        j+=1
    else:
        plt.text(nu[idx[i]], fgs[i][idx[i]], label[i], rotation=rot[i], color=col[i],fontsize=12)
plt.loglog(nu,sumf, "--", linewidth=4, color=col[-1])
plt.text(nu[idx[-1]], fgs[-1][idx[-1]]+scale[2], label[-1], rotation=rot[-1], color=col[-1],fontsize=12)

idx=30
color='k'
color2='C0'
xmin=10
xmax=1010
ymin=0.05
ymax=7e2
y_value=np.arange(1e-10,1e5,1)
plt.fill_betweenx(y_value, 24, 34, alpha=.2, color=color2)
plt.fill_betweenx(y_value, 39, 50, alpha=.2, color=color2)
plt.fill_betweenx(y_value, 60, 79, alpha=.2, color=color2)
plt.fill_betweenx(y_value, 81, 120, alpha=.2, color=color2)
plt.fill_betweenx(y_value, 121, 170, alpha=.2, color=color2)
plt.fill_betweenx(y_value, 180, 260, alpha=.2, color=color2)
plt.fill_betweenx(y_value, 300, 410, alpha=.2, color=color2)
plt.fill_betweenx(y_value, 450, 650, alpha=.2, color=color2)
plt.fill_betweenx(y_value, 700, 1010, alpha=.2, color=color2)
plt.text(30.,ymin, "30", color=color, alpha=0.5, ha='center', va='bottom', fontsize=12)
plt.text(44.,ymin, "44", color=color, alpha=0.5, ha='center', va='bottom', fontsize=12)
plt.text(70.,ymin, "70", color=color, alpha=0.5, ha='center', va='bottom', fontsize=12)
plt.text(100.,ymin, "100", color=color, alpha=0.5, ha='center', va='bottom', fontsize=12)
plt.text(143.,ymin, "143", color=color, alpha=0.5, ha='center', va='bottom', fontsize=12)
plt.text(217.,ymin, "217", color=color, alpha=0.5, ha='center', va='bottom', fontsize=12)
plt.text(353.,ymin, "353", color=color, alpha=0.5, ha='center', va='bottom', fontsize=12)
plt.text(545.,ymin, "545", color=color, alpha=0.5, ha='center', va='bottom', fontsize=12)
plt.text(857.,ymin, "857", color=color, alpha=0.5, ha='center', va='bottom', fontsize=12)

plt.axvline(x=115., color=color, alpha=0.2)
plt.axvline(x=230., color=color, alpha=0.2)
plt.axvline(x=345., color=color, alpha=0.2)
plt.text(115.,ymax, "CO 1-0", color=color, alpha=0.5, ha='right',va='top', fontsize=12,rotation=90)
plt.text(230.,ymax, "CO 2-1", color=color, alpha=0.5, ha='right',va='top', fontsize=12,rotation=90)
plt.text(345.,ymax, "CO 3-2", color=color, alpha=0.5, ha='right',va='top', fontsize=12,rotation=90)

plt.tick_params(axis='both', which='major', labelsize=16)
plt.ylabel(r"Brightness temperature [$\mu$K]",fontsize=18)
plt.xlabel(r"Frequency [GHz]",fontsize=18)
#plt.legend(["CMB", "Free-free", "Synchrotron", "Spinning Dust", "Thermal Dust", "Sum fg"], loc=6)
plt.xlim(xmin,xmax)
plt.ylim(ymin,ymax)
plt.tick_params(which="both",direction="in", labelleft='off', labelright='on', labeltop='off', labelbottom='off')
plt.savefig(dir+"figs/spec_params_npipe.png", bbox_inches='tight',  pad_inches=0.02)
plt.show()
"""

N = 1000
nu = np.linspace(0,1000,N)
CMB = cmb(nu*1e9,70)
FF = ff(nu*1e9, 100., 7000.)
SYNC = sync(nu*1e9,30.*1e6,1.)
SDUST = sdust(nu*1e9,100.,11.*1e9)
TDUST = tdust(nu*1e9,100,1.6,19.)
sumf = FF+SYNC+SDUST+TDUST
fgs=[CMB,FF,SYNC,SDUST,TDUST]
col=["C9","C0","C2","C1","C3","C7"]
label=["CMB","Free-Free","Synchrotron","Spinning Dust","Thermal Dust", "Sum fg."]
rot=[-2, -35, -45, -70, 27, -45]
idx=[15, 150, 120, 80, 20, 50]
#yidx=[0, 150, 150, 100, 300, 30]
scale=[7,2.3,180]
j=0
for i in range(len(fgs)):
    plt.loglog(nu,fgs[i], linewidth=4,color=col[i])
    if i==0 or i==4:
        plt.text(nu[idx[i]], fgs[i][idx[i]]+scale[j], label[i], rotation=rot[i], color=col[i],fontsize=12)
        j+=1
    else:
        plt.text(nu[idx[i]], fgs[i][idx[i]], label[i], rotation=rot[i], color=col[i],fontsize=12)
plt.loglog(nu,sumf, "--", linewidth=4, color=col[-1])
plt.text(nu[idx[-1]], fgs[-1][idx[-1]]+scale[2], label[-1], rotation=rot[-1], color=col[-1],fontsize=12)

idx=30
color='k'
color2='C0'
xmin=10
xmax=1010
ymin=0.05
ymax=7e2
y_value=np.arange(1e-10,1e5,1)
plt.fill_betweenx(y_value, 24, 34, alpha=.2, color=color2)
plt.fill_betweenx(y_value, 39, 50, alpha=.2, color=color2)
plt.fill_betweenx(y_value, 60, 79, alpha=.2, color=color2)
plt.fill_betweenx(y_value, 81, 120, alpha=.2, color=color2)
plt.fill_betweenx(y_value, 121, 170, alpha=.2, color=color2)
plt.fill_betweenx(y_value, 180, 260, alpha=.2, color=color2)
plt.fill_betweenx(y_value, 300, 410, alpha=.2, color=color2)
plt.fill_betweenx(y_value, 450, 650, alpha=.2, color=color2)
plt.fill_betweenx(y_value, 700, 1010, alpha=.2, color=color2)
plt.text(30.,ymin, "30", color=color, alpha=0.5, ha='center', va='bottom', fontsize=12)
plt.text(44.,ymin, "44", color=color, alpha=0.5, ha='center', va='bottom', fontsize=12)
plt.text(70.,ymin, "70", color=color, alpha=0.5, ha='center', va='bottom', fontsize=12)
plt.text(100.,ymin, "100", color=color, alpha=0.5, ha='center', va='bottom', fontsize=12)
plt.text(143.,ymin, "143", color=color, alpha=0.5, ha='center', va='bottom', fontsize=12)
plt.text(217.,ymin, "217", color=color, alpha=0.5, ha='center', va='bottom', fontsize=12)
plt.text(353.,ymin, "353", color=color, alpha=0.5, ha='center', va='bottom', fontsize=12)
plt.text(545.,ymin, "545", color=color, alpha=0.5, ha='center', va='bottom', fontsize=12)
plt.text(857.,ymin, "857", color=color, alpha=0.5, ha='center', va='bottom', fontsize=12)

plt.axvline(x=115., color=color, alpha=0.2)
plt.axvline(x=230., color=color, alpha=0.2)
plt.axvline(x=345., color=color, alpha=0.2)
plt.text(115.,ymax, "CO 1-0", color=color, alpha=0.5, ha='right',va='top', fontsize=12,rotation=90)
plt.text(230.,ymax, "CO 2-1", color=color, alpha=0.5, ha='right',va='top', fontsize=12,rotation=90)
plt.text(345.,ymax, "CO 3-2", color=color, alpha=0.5, ha='right',va='top', fontsize=12,rotation=90)

plt.tick_params(axis='both', which='major', labelsize=16)
plt.ylabel(r"Brightness temperature [$\mu$K]",fontsize=18)
plt.xlabel(r"Frequency [GHz]",fontsize=18)
#plt.legend(["CMB", "Free-free", "Synchrotron", "Spinning Dust", "Thermal Dust", "Sum fg"], loc=6)
plt.xlim(xmin,xmax)
plt.ylim(ymin,ymax)
plt.tick_params(which="both",direction="in", labelleft='off', labelright='on', labeltop='off', labelbottom='off')
plt.savefig(dir+"figs/spec_params_BIG.png", bbox_inches='tight',  pad_inches=0.02)
plt.show()
"""
# POLARIZATION


N = 1000
nu = np.linspace(0,1000,N)
CMB = cmb(nu*1e9,0.7)
SYNC = 0.05*sync(nu*1e9,30.*1e6,1.)
TDUST = tdust(nu*1e9,10,1.6,19.)
sumf = SYNC+TDUST
fgs=[CMB,SYNC,TDUST]
col=["C9","C2","C3","C7"]
label=["CMB","Synchrotron","Thermal Dust", "Sum fg."]
idx=[20, 100, 20, 60]
rot=[-2, -45, 27, -12]
scale=[0.07,0,.25,1.35]
j=0
for i in range(len(fgs)):
    plt.loglog(nu,fgs[i], linewidth=4,color=col[i])
    plt.text(nu[idx[i]], fgs[i][idx[i]]+scale[i], label[i], rotation=rot[i], color=col[i],fontsize=12)


plt.loglog(nu,sumf, "--", linewidth=4, color=col[-1])
plt.text(nu[idx[-1]], fgs[-1][idx[-1]]+scale[3], label[-1], rotation=rot[-1], color=col[-1],fontsize=12)

color='k'
color2='C0'
xmin=10
xmax=1010
ymin=0.05
ymax=7e2
y_value=np.arange(1e-10,1e5,1)
plt.fill_betweenx(y_value, 24, 34, alpha=.2, color=color2)
plt.fill_betweenx(y_value, 39, 50, alpha=.2, color=color2)
plt.fill_betweenx(y_value, 60, 79, alpha=.2, color=color2)
plt.fill_betweenx(y_value, 81, 120, alpha=.2, color=color2)
plt.fill_betweenx(y_value, 121, 170, alpha=.2, color=color2)
plt.fill_betweenx(y_value, 180, 260, alpha=.2, color=color2)
plt.fill_betweenx(y_value, 300, 410, alpha=.2, color=color2)
ymax1=ymax-50
plt.text(30.,ymax1, "30", color=color, alpha=0.5, ha='center', va='top', fontsize=12)
plt.text(44.,ymax1, "44", color=color, alpha=0.5, ha='center', va='top', fontsize=12)
plt.text(70.,ymax1, "70", color=color, alpha=0.5, ha='center', va='top', fontsize=12)
plt.text(100.,ymax1, "100", color=color, alpha=0.5, ha='center', va='top', fontsize=12)
plt.text(143.,ymax1, "143", color=color, alpha=0.5, ha='center', va='top', fontsize=12)
plt.text(217.,ymax1, "217", color=color, alpha=0.5, ha='center', va='top', fontsize=12)
plt.text(353.,ymax1, "353", color=color, alpha=0.5, ha='center', va='top', fontsize=12)

plt.tick_params(axis='both', which='major', labelsize=16)
plt.ylabel(r"Brightness temperature [$\mu$K]",fontsize=18)
plt.xlabel(r"Frequency [GHz]",fontsize=18)
#plt.legend(["CMB", "Synchrotron", "Thermal Dust", "Sum fg"], loc=6)
plt.xlim(xmin,xmax)
plt.ylim(ymin,ymax)
plt.tick_params(which="both",direction="in", labelleft='off', labelright='on', labeltop='off', labelbottom='off')
plt.savefig(dir+"figs/spec_params_P_BIG.pdf", bbox_inches='tight',  pad_inches=0.02)
plt.show()
"""
