import numpy as np
import matplotlib.pyplot as plt
import powerlaw
import sys

d=[-218.4458,
0.4004898, 0.1778779, 9.7997800E-02, 3.9183609E-02, 3.8629450E-02, 3.1717252E-02, 4.2692993E-02, 4.3908957E-02, 5.9714161E-02, 9.9677220E-02, 0.1017583, 9.8673873E-02, 0.1004481, 0.1267319, 0.1271955, 0.1258029, 0.1274267, 0.1272058, 0.1270577, 0.1268518, 0.1289727, 0.2887138]
f=[0.408, 22.8, 28.4, 33., 40.6, 40.6, 44.1, 60.8, 60.8, 70.3, 93.5, 93.5, 93.5, 93.5, 100., 100., 100., 100., 100., 100., 100., 100., 143.]
d2=[107.3353, 0.4481514, 0.1992134, 0.1069137, 4.3700784E-02, 4.3227028E-02, 3.5943400E-02, 4.4008739E-02, 4.5086958E-02, 6.2040720E-02, 0.1021026, 0.1042721, 0.1023647, 0.1032797, 0.1290995, 0.1294701, 0.1288557, 0.1302578, 0.1299172, 0.1297056, 0.1292863, 0.1312539, 0.2923834]



dir = "/Users/trygveleithesvalheim/Documents/jobb/jastro/masterplots/figs/spec_param/"
plt.style.use(u"trygveplot")
k_B = 1.3806503e-23
h = 6.62607004e-34
T_d = 18.2
beta = 1.57
nu_ref = 857e9
Tcmb = 2.7255      # K CMB Temperature
c      = h / (k_B*T_d)

file="unit_conversions.dat"
a2t = np.loadtxt(file,usecols=3)

file="gain_no0001.dat"
gains = np.loadtxt(file)[-1]
gains = gains[1:]

def sync(nu, As, alpha):
    #alpha = 1., As = 30 K (30*1e6 muK)
    nu_0 = 0.408*1e9 # 408 MHz
    fnu, f = np.loadtxt(dir+"Synchrotron_template_GHz_extended.txt", unpack=True)
    f = np.interp(nu, fnu*1e9, f)
    f0 = np.interp(nu_0, nu, f) # Value of s at nu_0

    s_s = As*(nu_0/nu)**2*f/f0
    return s_s

def sdust(nu, Asd, nup):
    #s_sd = Asd*(nu0/nu)**2*(fsd(nu*nup0/nup)/fsd(nu0*nup0/nup))
    #nup0=30.0*1e9
    nu_0 = 41.e9 #nu10=22.8*1e9, nu20=41.0*1e9
    fnu, f = np.loadtxt("spdust2_cnm.dat", unpack=True)
    # (nup0/nup) = 30./31. = 1.
    f = np.interp(nu, fnu*1e9, f)
    f0 = np.interp(nu_0, nu, f) # Value of s at nu_0
    s_sd = Asd*(nu_0/nu)**2*f/f0
    return s_sd

def ff(nu,EM,Te):
    #EM = 1 cm-3pc, Te= 500 #K
    T4 = Te/1e4
    nu9 = nu/1e9 #Hz
    g_ff = np.log(np.exp(5.960-np.sqrt(3)/np.pi*np.log(nu9*T4**(-3./2.)))+np.e)
    tau = 0.05468*Te**(-3./2.)*nu9**(-2)*EM*g_ff
    s_ff = 1e6*Te*(1-np.exp(-tau))
    return s_ff

def dust(nu):
    dust = (np.exp(c*nu_ref)-1.) / (np.exp(c*nu)-1.) * (nu/nu_ref)**(beta+1.)
    return dust

def dust2(nu, frac_flat):
    dust = (np.exp(c*nu_ref)-1.) / (np.exp(c*nu)-1.) * (nu/nu_ref)**(beta+1.)* (np.tanh(c*frac_flat*nu)/np.tanh(c*frac_flat*nu_ref))**(2-beta)
    return dust

def dust3(nu, frac_flat):
    dust = (np.exp(c*nu_ref)-1.) / (np.exp(c*nu)-1.) * (nu/nu_ref)**(beta+1.)* (np.tanh(c*frac_flat*nu)/np.tanh(c*frac_flat*nu_ref))
    return dust


nu = np.linspace(0.4,1000,1000)*1e9

#freefree
#FF = ff(nu, 100., 7000.)
SYNC = sync(nu,30.*1e6,1.)

plt.loglog(nu/1e9,dust(nu), label = "Standard")

for i in [6]:
    plt.loglog(nu/1e9,dust2(nu,i),label="dust2 alpha = "+str(i))


plt.loglog(nu/1e9,dust3(nu,6),label="dust3 alpha = "+str(6))


"""
fit = powerlaw.Fit(dust(nu)[:30])
print fit.alpha
fit = powerlaw.Fit(dust2(nu,3.25)[:30])
print fit.alpha
fit = powerlaw.Fit(dust3(nu,6)[:30])
print fit.alpha
"""

#plt.loglog(nu/1e9,(nu/1e10)**1.6*dust(nu)[0],color="grey", label="Powerlaw 1.6",alpha=0.8)
#plt.loglog(nu/1e9,(nu/1e10)**2.0*dust2(nu,3.25)[0],color="grey", label="Powerlaw 2.0",alpha=0.8)
#plt.loglog(nu/1e9,(nu/1e10)**2.6*dust3(nu,6)[0],color="grey", label="Powerlaw 2.6",alpha=0.8)


file=str(sys.argv[1])
lol = np.loadtxt(file)
def column(matrix, i):
    return [row[i] for row in matrix]



lol[:,1] = (lol[:,1])/gains
sort = sorted(lol, key=lambda a : a[0])

x = np.asarray(column(sort, 0))
y = np.asarray(column(sort, 1))
#y[:]=y[:]+100.
data = (y/(y[-1]/a2t[-1])*dust2(x[-1]*1e9,2))/a2t

#lens =  np.histogram(x,bins = )
#data =  np.histogram(x, weights = data)
#print data/lens
#plt.loglog(x,data,"-o",label="Normalized data")
plt.loglog(f, d,"-o", label="Templates")
plt.loglog(f, d2,"-o", label="Templates 2")

y_value=np.arange(1e-10,1e5,1)
color='k'
color2='C0'
ymin=5
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

plt.legend(loc="lower right")
plt.xlim([0.4,900])
#plt.ylim([1e-3, 5])#100000])
plt.show()
