
from math import *
import matplotlib.pylab as plt
import numpy as np
from matplotlib.mlab import bivariate_normal
import scipy.stats as stats

# the core of the method: sample recursively from two normal distributions
# Tthe mean for the current sample, is updated at each step.

n = 10000
rho=0.8 #correlation
#Means
m1 = 0.
m2 = 0.
cov_test = np.array([[1,rho],
                     [rho,1]])
#Standard deviations
s1 = 1.
s2 = 1.

# Distribution Variables
sd=sqrt(1-rho**2) #stddev
s1sd = s1 * sd
s2sd = s2 * sd
rx = rho / s2
ry = rho / s1

#Initialize vectors
x=np.zeros(n)-4
y=np.zeros(n)

burnin = int(n/4) # When to start saving
thetas = np.zeros((n-burnin,2)) # Saving data

for i in range(n): # Sampling from all the different variables for each pixel
    x[i] = np.random.normal(m1+rx*(y[i-1]-m2),s1sd)
    y[i] = np.random.normal(m2+ry*(x[i]-m1),s2sd)

    if i >= burnin: # Burn-in values
        thetas[i-burnin,0] = x[i]
        thetas[i-burnin,1] = y[i]

# Bivariate normal distribution for Model
x1 = np.arange(-5.0, 5.0, 0.1)
y1 = np.arange(-5.0, 5.0, 0.1)
xx, yy = np.meshgrid(x1, y1)
zz = bivariate_normal(xx, yy, s1, s2, m1, m2, rho)

# Plotting
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
# Remove the tick marks; they are unnecessary with the tick lines we just plotted.
plt.tick_params(axis="both", which="both", bottom="off", top="off",
                labelbottom="on", left="off", right="off", labelleft="on")

ax.minorticks_on()
ax.yaxis.grid()
ax.yaxis.grid(b=True, which='minor', alpha=0.2)

#ax.plot(range(len(x)), x,range(len(y)), y )

# Posterior gibbs
kde = stats.gaussian_kde(thetas.T)
XY = np.vstack([xx.ravel(), yy.ravel()])
posterior_gibbs = kde(XY).reshape(xx.shape)

burn = ax.plot(x,y, alpha=0.5, label = 'Steps')                   # Full gibbs
postburn = ax.scatter(thetas[:,0],thetas[:,1])

likelihood = ax.contour(xx,yy,zz,linestyles = 'dashed', label="Likelihood")             # Univariate normal
posterior = ax.contour(xx,yy,posterior_gibbs,label="Posterior") # Posterior contour
plt.legend([burn, postburn, likelihood.collections[0],posterior.collections[0]],['Steps','Post Burn-in','Likelihood','Posterior'], loc="lower right")
plt.title(r'Gibbs sampler on Bivariate Normal distribution ($\rho=0.8$)')
plt.xlabel('x')
plt.ylabel('y')
plt.savefig('figs/gibbs.pdf', bbox_inches='tight',pad_inches=0.106)

plt.show()
