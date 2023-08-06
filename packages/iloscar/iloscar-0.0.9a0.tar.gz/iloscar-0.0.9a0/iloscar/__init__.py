from iloscar.app import iloscar_run

import os
import numpy as np

location = os.path.dirname(os.path.realpath(__file__))
dat0 = np.loadtxt(os.path.join(location, 'dat_y0', 'preind_steady.dat'))
dat1 = np.loadtxt(os.path.join(location, 'dat_y0', 'petm_steady.dat'))

np.savetxt('preind_steady.dat', dat0)
np.savetxt('petm_steady.dat', dat1)
