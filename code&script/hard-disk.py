#!/usr/bin/env python

from hoomd import *
from hoomd import hpmc
import numpy as np

# init & param
c = context.initialize()
sqrtN = int(option.get_user()[0])
phi = float(option.get_user()[1])
seed  = int(option.get_user()[2])
fname0 = 'N{0:d}_phi{1:4.3f}'.format(sqrtN**2, phi)

# init config
a = np.sqrt((np.pi/4.0)/phi)
system = init.create_lattice(unitcell=lattice.sq(a=a), n=sqrtN)

# MC setup
mc = hpmc.integrate.sphere(seed=seed)
mc.shape_param.set('A', diameter=1.0)

# log setup
log = analyze.log(filename=fname0+'.log', period=1e4, quantities=['hpmc_sweep', 
                                                                  'hpmc_translate_acceptance', 
                                                                  'hpmc_d'], phase=0)
# autotune
tuner = hpmc.util.tune(obj=mc, tunables=['d'], max_val=[0.5], target=0.2)
for i in range(100):
    run(100, quiet=True)
    tuner.update()
run(1e4)
    
# run & dump
sdf= hpmc.analyze.sdf(mc=mc, filename='sdf_'+fname0+'.dat', xmax=0.02, dx=1e-4, navg=2000, period=50)
#re = dump.gsd(filename='restart_'+fname0+'.gsd', period=1e6, group=group.all(), truncate=True)
dp = dump.gsd(filename='dump_'+fname0+'.gsd', period=1e5, group=group.all())
run(1e8)

