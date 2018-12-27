from __future__ import division, print_function
import sys
import gsd
import gsd.hoomd
import freud
import numpy as np
import matplotlib.pyplot as plt


if __name__=='__main__':

    fn_in  = sys.argv[1]
    j = int(sys.argv[2])
    #fn_out = sys.argv[2]
    #istart = int(sys.argv[3])
    #iend   = int(sys.argv[4])

    config = gsd.hoomd.open(fn_in, 'rb')
    Nframe = len(config)
    
    l_box  = config[0].configuration.box[:2]
    freud_box = freud.box.Box(Lx=l_box[0], Ly=l_box[1], is2D=True)
    hex_order = freud.order.HexOrderParameter(rmax=1.2, k=6, n=6)
    
    pos = config[j].particles.position
    hex_order.compute(freud_box, pos)

    psi6 = hex_order.psi
    ave_psi6 = np.mean(psi6)
    relative_angles = np.angle(psi6) - np.angle(ave_psi6)
    #print(j, abs(ave_psi6), file=open(fn_out, 'a'))
    
    fig = plt.scatter(pos[:,0], pos[:,1], c=abs(relative_angles), cmap='viridis', vmin=0.0, vmax=np.pi, s=2.5, lw=0)
    #plt.colorbar(fig)
    plt.axes().set_aspect('equal')
    plt.axis('off')

    plt.show()

