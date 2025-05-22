'''
A script to run wget to obtain images for the dwarfs needed for the 
A118 Assignment 3 project

Ultra-Faint Dwarfs:
- Leo IV
- Hercules
- Ursa Major I
- Canis Venatici II
- Bootes I
- Coma Berenices

Filters:
- F606W
- F814W

'''

import numpy as np
import os
import glob
import shutil as sh

UFD_NAMES = ['leoiv','hercules','ursamajori','comaberenices','canesvenaticiii','bootesi']
SINGLEFIELD = ['leoiv','canesvenaticiii']
BANDS = ['f606w','f814w']


if __name__ == '__main__':
    cmd = 'wget https://archive.stsci.edu/hlsps/fhufd/hlsp_fhufd_hst_acs_{d}_{b}_v2.0_drz.fits'

    for name in UFD_NAMES:
        for band in BANDS:
            if name not in SINGLEFIELD:
                cmd.format(d=name+'01',b=band)
                os.system(cmd)
            else:
                cmd.format(d=name,b=band)
                os.system(cmd)

    current_dir = os.getcwd()
    files = glob.glob(current_dir+'/*.fits')

    for file in files:
        cmd = f'mv {file} images/dwarfs/'
        os.system(cmd)

    print('HST Files downloaded succesfully!')
