'''
Script to run photometry on ultra-faint dwarfs using photutils
'''

# basic packages
import numpy as np
import pandas as pd
import os
import glob
import logging

# astropy stuff
from astropy.stats import sigma_clipped_stats 
from astropy.visualization import SqrtStretch, LinearStretch, LogStretch 
from astropy.visualization.mpl_normalize import ImageNormalize 
import astropy.io.fits as pyfits
from astropy.table import Table

# photutils !!
import photutils as ph



# FUNCTIONS

def find_sources(im,sig, ):
    return
def calculate_flux(im,srcs,):
   return 
if __name__ == '__main__':
    logger = logging.Logger()
    