#!/usr/bin/env python

import sys
import numpy as np
#import matplotlib.pyplot as plt

def extrapolate(s, dx, xmax, degree=5):
    n_fit = int(np.ceil(xmax/dx))
    s_fit = s[0:n_fit]
    x_fit = np.arange(0, xmax, dx) + dx/2.0
    
    p = np.polyfit(x_fit, s_fit, degree)
    
    return np.polyval(p, 0.0)


if __name__=='__main__':
    
    dx = 1e-4
    xmax = 0.02
    filename = sys.argv[1]
    phi = float(sys.argv[2])
    istart = int(sys.argv[3])
    
    data = np.loadtxt(filename)
    rows = np.size(data[:,0])
    s0 = np.empty(rows)
    steps = data[:,0]
    
    x_fit = np.arange(0, xmax, dx) + dx/2.0
    for i in range(rows):
        #s0[i] = extrapolate(data[i,1:], dx, xmax, 5)
        #s0[i] = np.polyval( np.polyfit(x_fit[10:], data[i,11:], 5), 0.0 )
        s0[i] = np.polyval( np.polyfit(x_fit[:], data[i,1:], 5), 0.0 )
        
    p = (4.0*phi/np.pi) * (1.0 + s0/4.0)
    np.savetxt('tmp', [[phi, np.mean(p), np.std(p)]])
    np.savetxt('tmp_equi', [[phi, np.mean(p[istart:]), np.std(p[istart:])]])
    np.savetxt('tmp_p', p)

    #fig, ax = plt.subplots()
    #ax.plot(steps, p, marker='.')
    #fig.savefig('p.png')
    
