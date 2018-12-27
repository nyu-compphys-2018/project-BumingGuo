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

    data_all = np.c_[phi, p]
    delta = []
    Ngrid = []
    for i in range(9,15):
        n = 2**i
        fn = 'phi_cid_std_fluc_'+str(i)+'.dat'
        data_cid = np.loadtxt(fn)
        cid = data_cid[:,1] * n**2 * n**0.5
        data_all = np.c_[data_all, cid]

        delta.append( np.sqrt(V[7])/n )
        Ngrid.append(n)


    S_reduced = np.delete(S, [10])
    mx = data_all[:,2:]
    mx = np.delete(mx, (10), axis=0)
    dim_m = len(mx[0,:])
    dim_n = len(mx[:,0])

    m1 = np.zeros((dim_m+1,dim_m+1))
    m1[1:,1:] = dim_n * np.identity(dim_m)
    m1[0,1:]  = np.sum(mx, axis=0)
    m1[1:,0]  = m1[0,1:]
    m1[0,0]   = np.sum(mx**2) 

    v2 = np.zeros(dim_m+1)
    v2[1:] = np.sum(S_reduced)
    v2[0]  = np.sum( np.dot( np.transpose(mx), S_reduced ) )

    v1 = np.dot( np.linalg.inv(m1), v2 )

    fig, ax = plt.subplots(2,2)
    collapse = np.c_[phi, p]
    for i in range(9,15):
        ax[0,1].plot(phi, data_all[:,i-7] * v1[0] + v1[i-8], marker='.')
        collapse = np.c_[collapse, data_all[:,i-7] * v1[0] + v1[i-8]]

    print(v1[0])
    np.savetxt('coeB.dat', np.c_[Ngrid, delta, v1[1:]])
    np.savetxt('fit_phi_p_S.dat', np.c_[phi_plt, p_plt, S_plt])
    np.savetxt('collapse.dat', collapse)
    
    ax[0,0].plot(phi, p, marker='.')
    ax[0,0].plot(phi_plt, p_plt)
    ax[0,1].plot(phi_plt, S_plt)
    #ax[1,0].plot(Ngrid, A, marker='.')
    #ax[1,0].plot(delta, A, marker='.')
    #ax[1,0].set_xscale('log')
    #ax[1,0].set_yscale('log')
    ax[1,1].plot(delta, v1[1:], marker='.')
    ax[1,1].set_xscale('log')
    ax[1,1].set_yscale('log')

    plt.show()
