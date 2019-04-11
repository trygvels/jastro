import numpy as np
import matplotlib.pyplot as plt

frac_flat = 5.2
nu_flat = 100e9
nu_ref = 857e9
h     = 6.626e-34
c     = 3.0e+8
k     = 1.38e-23
Td = 19.
beta = 1.6
x      = h / (k*Td)

nu = np.linspace(20, 1000, 1000)*1e9

nu_steep = nu_flat 
delta    = -frac_flat

dust=np.zeros(1000)
def d(nu, beta, T):
    for i in range(len(dust)):  
        if nu[i] > nu_steep:
            dust[i] = (np.exp(x*nu_ref)-1.0) / (np.exp(x*nu[i])-1.0) * (nu[i]/nu_ref)**(beta+1.0)
        else:
            dust[i] = (np.exp(x*nu_steep)-1.0) / (np.exp(x*nu[i])-1.0) * (nu[i]/nu_steep)**(beta+1.0+delta) * (np.exp(x*nu_ref)-1.0) / (np.exp(x*nu_steep)-1.0) * (nu_steep/nu_ref)**(beta+1.0)
    return dust
plt.ylim([1e-3,2])
plt.loglog(nu/1e9, d(nu,beta,Td))
plt.show()
