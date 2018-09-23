
from math import *
import matplotlib.pylab as plt
import numpy as np
from matplotlib.mlab import bivariate_normal
import scipy.stats as stats
from scipy.interpolate import interp1d
import corner

class modified_blackbody:
    #np.random.seed(1234)

    """
    Denne funksjonen du nå har kalles et modifisert blackbody-spektrum,
    og er en veldig god tilnærming for frekvensspekteret til stov.
    Den har tre frie parametere, nemlig amplituden A relativt til frekvensen nu_0,
    indeksen beta (som angir helningen til spekteret),
    og temperatur T (som angir hvor toppen til spekteret ligger).
    """

    def __init__(self,nus):
        self.nus   = nus        # FrekvensER
        self.A    = 100.        # muK er en amplitude-parameter
        self.beta = 1.6         # er en spektral-indeks
        self.T    = 19.         # K er en stov-temperatur
        self.nu_0 = 857.    # GHz er en fiksert referanse-frekvens
        self.h    = 6.62607e-34 # Planck's konstant
        self.k_b  = 1.38065e-23 # Boltzmanns konstant
        self.Tcmb = 2.7255      # K CMB Temperature

        self.K = self.h*1e9/self.k_b # Constant


    def s_nu(self, nu):
        # Signalet i hver piksel er gitt av modellen:
        #self.g(nu)!!!
        s = self.A*(nu/self.nu_0)**(self.beta+1)*(np.exp(self.K*self.nu_0/self.T) - 1.)/ (np.exp(self.K*nu/self.T) - 1.)
        return s

    def g(self,nu): # konverteringsfaktoren mellom termodynamisk og brightness-temperatur.
        x = self.K*nu/self.Tcmb
        return (np.exp(x)-1)**2 / (x**2 * np.exp(x))

    def d_nu(self,nu): # Legg på Gaussisk tilfeldig stoy per frekvens med et standardavvik på f.eks. 10% av signalet
        s_nu = self.s_nu(nu)
        sigma_n = 0.1*s_nu # Redundant?
        n_nu = np.random.normal(0, sigma_n)
        d_nu = s_nu + n_nu #Adding noise
        return d_nu


    def inverse(self, c1, c2, con, d):
        N = 1000
        xs = np.linspace(c1,c2,N) # This is either betas or Ts
        P = np.zeros((len(self.nus),N))

        i = 0 #counter
        # Super fast version (But is it correct?)
        for nu in self.nus:
            if con==0:
                self.beta = xs
            else:
                self.T = xs

            s = self.s_nu(nu)
            sigma = 0.1*s
            P[i,:] = -(d[i]-s)**2/(2*sigma**2)
            i+=1

        Px = np.exp(np.sum(P, axis = 0))

        dx = abs(xs[1]-xs[0])
        Fx = np.cumsum(Px*dx)
        eta = np.random.uniform(0.,max(Fx))
        f = interp1d(Fx, xs)
        return f(eta)


    def gibbs(self):
        # The mean for the current sample, is updated at each step.
        n = 1000000

        d = self.d_nu(self.nus) # This should be measured pixel value
        burnin = int(n/4) # When to start saving
        thetas = np.zeros((n-burnin,3)) # Saving data

        for i in range(n): # Sampling

            if not i%1000:
                print "---- Iteration", i, " -----"
                print "A", self.A
                print "beta", self.beta
                print "T", self.T

            ##############
            # Sampling A #
            ##############
            s = self.s_nu(self.nus) # MAKE THIS DEPENDANT ON A, B, T
            sigma_n = 0.1*s # sigma_n = 10 prosent av s
            Y = s/self.A # self.Y(self.nus)
            a1 = sum(d*Y/(sigma_n)**2)
            a2 = sum((Y/sigma_n)**2)
            self.A = np.random.normal(a1/a2, 1/np.sqrt(a2)) # P(A|d,beta,T)
            #self.A = np.random.normal(100., 0.1)

            #################
            # Sampling Beta #
            #################
            self.beta = self.inverse(1.,3.,0, d)
            #self.beta = np.random.normal(1.6, 0.01)

            ##############
            # Sampling T #
            ##############
            self.T = self.inverse(1.,50.,1, d)
            #self.T = np.random.normal(19., 0.01)

            if i >= burnin: # Burn-in values
                thetas[i-burnin,0] = self.A
                thetas[i-burnin,1] = self.beta
                thetas[i-burnin,2] = self.T
        return thetas

if __name__ ==  "__main__":
    # Lag deg et simulert datasett som består av data på 9 frekvenser
    # (30,44,70,100,143,217,353,545 og 857 GHz) med en enkelt piksel.

    nus = np.array([30,44,70,100,143,217,353,545,857]) #GHz
    spec = modified_blackbody(nus)


    print "Gibbs sampling"
    thetas = spec.gibbs()
    print "Plotting"
    fig = corner.corner(thetas,color='g', labels=[r"$A$", r"$\beta$", r"$T$"],show_titles=True, title_kwargs={"fontsize": 12})
    plt.tight_layout()
    plt.show()

    """
    ss = spec.s_nu(nus)
    plt.loglog(nus,ss, "-o")
    plt.xlabel(r'$\nu$ [GHz]')
    plt.ylabel('s')
    plt.show()

    plt.plot(range(len(thetas[:,0])),thetas[:,0], "-o")
    plt.show()

    plt.hist(thetas[:,0],50)
    plt.xlabel('A')
    plt.show()
    """
