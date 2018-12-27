#!/usr/bin/env python
from __future__ import division, print_function
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


if __name__=='__main__':
    
    N = 256*256
    data = np.loadtxt('phi_p_std.dat')

    phi = data[:,0]
    p = data[:,1]
    V = N*np.pi/(4.0*phi)

    pfit = np.polyfit(V[:], p[:], 6)
    pfit_s = np.polyfit(V[:], p[:], 6)
    pfit_s[-1] -= np.polyval(pfit, N*np.pi/(4.0*0.693))
    pint = np.polyint(pfit_s)

    phi_plt = np.linspace(0.695, 0.721, 100)
    V_plt = N*np.pi/(4.0*phi_plt)
    p_plt = np.polyval(pfit, V_plt)
    
    S0 = np.polyval(pint, N*np.pi/(4.0*0.75))
    S_plt = np.polyval(pint, V_plt) - S0
    S = np.polyval(pint, V) - S0

    fig, ax = plt.subplots(2,2)
    collapse = np.c_[phi, p]
    data_all = np.c_[phi, p]
    cid_line = []
    S_line = []
    A = []
    B = []
    delta = []
    Ngrid = []
    S_reduced = np.delete(S, [10])
    for i in range(9,15):
        n = 2**i
        fn = 'phi_cid_std_fluc_'+str(i)+'.dat'
        data_cid = np.loadtxt(fn)
        #cid = data_cid[:,1] * n**2
        cid = data_cid[:,1] * n**2 * n**0.5
        data_all = np.c_[data_all, cid]
        #cid = data_cid[:,1]
        cid_reduced = np.delete(cid, [10])

        cid_line = np.r_[cid_line, cid_reduced]
        S_line = np.r_[S_line, S_reduced]
        
        slope,intercept,_,_,_ = stats.linregress(cid_reduced, S_reduced)
        A.append(slope)
        B.append(intercept)
        delta.append( np.sqrt(V[7])/2**i )
        Ngrid.append(n)

        #ax[0,1].plot(phi, cid+intercept, marker='.')
        #ax[0,1].plot(phi, cid*slope+intercept, marker='.')
        collapse = np.c_[collapse, cid*slope+intercept]

    np.savetxt('coe.dat', np.c_[Ngrid, delta, A, B])
    np.savetxt('fit_phi_p_S.dat', np.c_[phi_plt, p_plt, S_plt])
    np.savetxt('collapse.dat', collapse)
    
    slope,intercept,_,_,_ = stats.linregress(cid_line, S_line)
    
    for i in range(9,15):
        ax[0,1].plot(phi, data_all[:,i-7]*slope+intercept, marker='.')
        #ax[0,1].plot(phi, data_all[:,i-7]*A[0]+B[i-9], marker='.')

    ax[0,0].plot(phi, p, marker='.')
    ax[0,0].plot(phi_plt, p_plt)
    ax[0,1].plot(phi_plt, S_plt)
    ax[1,0].plot(Ngrid, A, marker='.')
    #ax[1,0].plot(delta, A, marker='.')
    ax[1,0].set_xscale('log')
    ax[1,0].set_yscale('log')
    ax[1,1].plot(delta, B, marker='.')
    ax[1,1].set_xscale('log')
    ax[1,1].set_yscale('log')

    fig, ax1 = plt.subplots()
    ax1.plot(cid_line, S_line, marker='.', ls='')

    plt.show()
