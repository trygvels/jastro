
from math import *
import matplotlib.pylab as plt
import numpy as np
from matplotlib.mlab import bivariate_normal
import scipy.stats as stats


nus   = np.array([30,44,70,100,143,217,353,545,857])#*1e9 #GHz FrekvensER
A    = 100.        # muK er en amplitude-parameter
beta = 1.6         # er en spektral-indeks
T    = 19.         # K er en stov-temperatur
nu_0 = 857.        # GHz er en fiksert referanse-frekvens
h    = 6.62607e-34 # Planck's konstant
k_b  = 1.38065e-23 # Boltzmanns konstant
Tcmb = 2.7255      # K CMB Temperature


def g(nu): # konverteringsfaktoren mellom termodynamisk og brightness-temperatur.
    x = h*nu/(k_b*Tcmb)
    return (np.exp(x)-1)**2 / (x**2 * np.exp(x))

def s_nu(nu):
    s = A*g(nu)*(nu/nu_0)**(beta+1)*(np.exp(h*nu_0/(k_b*T)) -1.)/ (np.exp(h*nu/(k_b*T))-1.)
    return s


def d_nu(nu): # Legg på Gaussisk tilfeldig stoy per frekvens med et standardavvik på f.eks. 10% av signalet
    s = s_nu(nu)
    sigma = 0.01*s # Redundant?
    n_nu = np.random.normal(0, sigma)
    d = s + n_nu #Adding noise
    return d_nu

def Y(self, nu):
    Y = (nu/nu_0)**(beta+1)*(np.exp(h*nu_0/(k_b*T)) -1.)/ (np.exp(h*nu/(k_b*T))-1.)
    return Y

n = 1000

#Initialize vectors
A    = np.zeros(n) + A
beta = np.zeros(n) + beta
T    = np.zeros(n) + T
d = d_nu(nus) # This should be measured pixel value
print d
burnin = int(n/4) # When to start saving
thetas = np.zeros((n-burnin,2)) # Saving data
#print nus
#print nus

for i in range(n): # Sampling

    ############
    # Sampling A
    ############
    s = s_nu(nus)
    sigma = 0.01*s
    a1 = sum(d*Y(nus)/(sigma)**2)
    a2 = sum((Y(nus)/(sigma))**2)
    A[i] = np.random.normal(a1/a2, 1/np.sqrt(a2)) # P(A|d,beta,T)
    A = A[i]
    #print "A_tilde:", a1/a2
    #print "A:", A

    ###############
    # Sampling Beta
    ###############

    beta[i] = np.random.normal(1.6, 0.1)
    beta = beta[i]

    ############
    # Sampling T
    ############
    T[i] = np.random.normal(19., 0.1)
    T = T[i]




    if i >= burnin: # Burn-in values
        thetas[i-burnin,0] = A[i]
        thetas[i-burnin,1] = beta[i]
        #thetas[i-burnin,2] = T[i]

# Lag deg et simulert datasett som består av data på 9 frekvenser
# (30,44,70,100,143,217,353,545 og 857 GHz) med en enkelt piksel.

nus = np.array([30,44,70,100,143,217,353,545,857])#*1e9 #GHz

#nus =  np.linspace(0, 10000, 100)

ss = s_nu(nus)

plt.loglog(nus,ss, "-o")
plt.xlabel(r'$\nu$ [GHz]')
plt.ylabel('s')
plt.show()

print "Gibbs sampling"
thetas = spec.gibbs()


"""
plt.plot(range(len(thetas[:,0])),thetas[:,0], "-o")
plt.show()


plt.hist(thetas[:,0],50)
plt.xlabel('A')
plt.show()
"""


plt.scatter(thetas[:,0],thetas[:,1])
plt.xlabel('A')
plt.ylabel(r'$\beta$')
plt.show()



"""
3) Oppgaven din nå er å sample 3D-distribusjonen P(A, beta, T|d) med en Gibbs sampler.
Men først må du utlede hva distribusjonen er for de tre kondisjonalene, dvs.

P(A | d, beta, T)
P(beta | d, A, T)
P(T | d, A, beta)

For å gjøre det, så husk at

n_nu = d_nu - s_nu(A, beta, T)

og P(n_nu) = N(0, sigma^2)

Du vil få ett type uttrykk for P(A|d, ...), som har en pen analytisk løsning,
mens P(beta|d..) og P(T|d...) begge må regnes ut numerisk,
og så samples via en inversion sampler eller tilsvarende.

Men start med P(A|d...), og anta at du vet nøyaktig hva beta og T, så får du det første steget til å funke greit.
"""
