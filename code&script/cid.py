from __future__ import division, print_function
import sys
import gsd
import gsd.hoomd
import numpy as np
from numba import jit
from sweetsourcod.lempel_ziv import lempel_ziv_complexity
from sweetsourcod.hilbert import get_hilbert_mask


@jit(nopython=True)
def mask_array(lattice, mask):
    return np.array([lattice[i] for i in mask])


def get_CID(c, nsites):
    hl = (c * np.log2(c) + 2 * c * np.log2(nsites / c)) / nsites
    return hl


@jit(nopython=True)
def _get_lattice_index(lattice_coordinates, lattice_boxv):
    ndim = len(lattice_boxv)
    x = lattice_coordinates
    if ndim == 1:
        return x[0]
    elif ndim == 2:
        return x[0] + lattice_boxv[0] * x[1]
    elif ndim == 3:
        return x[0] + lattice_boxv[0] * x[1] + lattice_boxv[0] * lattice_boxv[1] * x[2]
    else:
        raise NotImplementedError


@jit
def get_image(lattice_coords, lattice_boxv):
    image = np.zeros(np.prod(lattice_boxv), dtype=int)
    for j in xrange(lattice_coords.shape[0]):
        idx = _get_lattice_index(lattice_coords[j,:], lattice_boxv)
        image[idx] = 1
    return image


if __name__ == '__main__':

    fn_in = sys.argv[1]
    fn_out = sys.argv[2]
    log2N = int(sys.argv[3])
    istart = int(sys.argv[4])

    config = gsd.hoomd.open(fn_in, 'rb')
    Nframe = len(config)
    Nptcle = config[0].particles.N
    l_box = config[0].configuration.box[:2]

    Ngrid = 2**log2N
    lattice_boxv = np.array([Ngrid, Ngrid])
    hilbert_mask = get_hilbert_mask(lattice_boxv)
    n = np.prod(lattice_boxv)
    bin_size = l_box[0] / Ngrid

    for i in xrange(istart, Nframe):
        lattice_coords = np.floor(
            config[i].particles.position[:, :2] / bin_size).astype('int')
        image_raster = get_image(lattice_coords, lattice_boxv)
        image_hilbert = mask_array(image_raster, hilbert_mask).astype('uint8')

        c_lz77, _ = lempel_ziv_complexity(image_hilbert, 'lz77')
        CID_lz77 = get_CID(c_lz77, n)

        print(CID_lz77, file=open(fn_out, 'a'))
