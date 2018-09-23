import matplotlib.pyplot as plt
import numpy as np

def cmb(nu, A):
    T_cmb = 2.7255
    x = h*nu/(k_b*T_cmb)
    g = (np.exp(x)-1)**2/(x**2*np.exp(x))
    s_cmb = A_cmb/g
    return s_cmb

# WHAT IS f_s(nu??)
def sync(nu, A_s, alpha):
    nu_0 = 408 #MHz
    #f_s = ext template
    s_s = A_s*(nu_0/nu)**2*(f_s(nu/alpha)/f_s(nu_0/alpha))
    return s_s


def ff(nu,logEM,T_e):
    #logEM uni(-inf, inf)
    T_4 = T_e/1e4
    nu_9 = nu/1e9 #Hz
    g_ff = log(np.exp(5.960-np.sqrt(3)/np.pi*log(nu_9*T_4**(-3./2.))+np.e)
    tau = 0.05468*T_e**(-3./2.)*v_9**(-2)*EM*g_ff
    s_ff = 1e6*T_e*(1-e**(-tau))
    return s_ff

def sdust()
