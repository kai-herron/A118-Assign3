'''
Plot the output of Quinn's photometry

'''

__author__ = 'Kai Herron'

# basic packages
import numpy as np
import pandas as pd
import os
import glob
import logging
import matplotlib.pyplot as plt

# astropy stuff
from astropy.stats import sigma_clipped_stats 
from astropy.visualization import SqrtStretch, LinearStretch, LogStretch 
from astropy.visualization.mpl_normalize import ImageNormalize 
import astropy.io.fits as pyfits
from astropy.table import Table

# photutils !!
import photutils as ph

# isochrones !!
from fortranformat import FortranRecordReader as fread
from numpy import int32, float64, zeros, array

# declare some global variables
UFD_NAMES = ['Leo IV','Hercules','Ursa Major I','Coma Berenices','Canes Venatici II','Bootes I']
BANDS = ['F606W','F814W']


class DSED_Isochrones:
    """Holds the contents of a Dartmouth isochrone file."""

    #reads in a file and sets a few basic quantities
    def __init__(self,filename):
        self.filename=filename.strip()
        try:
            self.read_iso_file()
            self.columns=self.data[0].dtype.names
        except IOError:
            print("Failed to open isochrone file: ")
            print(self.filename)
            
    #this function reads in the standard isochrone format with mags
    def read_iso_file(self):
        #open file
        with open(self.filename,mode='r') as f:
            #define some line formats
            first_line=fread('(16X,I2,6X,I2)')
            third_line=fread('(1X,F7.4,F8.4,E11.4,E11.4,F7.2,F7.2)')
            fifth_line=fread('(25x,A51)')
            age_eep_line=fread('(5X,F6.3,6X,I3)')
            def column_line(mags): 
                return fread('(1x,a3,3x,a4,4x,a7,2x,a4,3x,a7,1x,{:d}a8)'.format(int(mags)))

            self.num_ages,num_mags=first_line.read(f.readline())
            self.num_cols = 5 + num_mags
            f.readline()
            f.readline()
            self.mixl,self.Y,self.Z,Zeff,self.FeH,self.aFe=third_line.read(f.readline())
            f.readline()
            self.system=fifth_line.read(f.readline())
            f.readline()

            ages=[]
            iso_set=[]
            for iage in range(self.num_ages):
                #read individual header and set up the isochrone container
                age,num_eeps=age_eep_line.read(f.readline())
                ages.append(age)
                names=column_line(num_mags).read(f.readline())
                #do some polishing:
                names=[name.replace('/','_') for name in names]
                names=[name[0:name.find('.')] if name.find('.') > 0 else name for name in names]
                names=tuple(names)
                formats=tuple([int32]+[float64 for i in range(self.num_cols-1)])
                iso=zeros(num_eeps,{'names':names,'formats':formats})
                for eep in range(num_eeps):
                    x=f.readline().split()
                    y=[]
                    y.append(int(x[0]))
                    [y.append(z) for z in map(float64,x[1:])]
                    iso[eep]=tuple(y)
                if iage < self.num_ages-1:
                    f.readline()
                    f.readline()
                iso_set.append(iso)
            self.ages=array(ages)
            self.data=array(iso_set,dtype=object)
            return True

def plot_one(model,ax,distance_modulus=0.0,reddening=0.0):
  for iso in model.data:
    ax.plot(iso['F606W   ']-iso['F814W   ']+reddening, iso['F814W   ']+distance_modulus, color='Black', lw=0.)


if __name__ == '__main__':
    # let's log stuff
    logging.getLogger().setLevel(logging.DEBUG)

    logging.info("Downloading photometry from HST...")
    phot_data = pd.read_csv('PATH_TO_FILE.csv')

    logging.info('Reading in isochrones...')
    iso = DSED_Isochrones(os.path.split(os.getcwd())[0]+'/data/isochrones/PYXIS.model')

    fig, axs = plt.subplot(nrows=2,ncols=3,figsize=(8.5,8.5))

    for i, ax in enumerate(axs):

        logging.info('Making plot for:{}'.format(UFD_NAMES[i]))
        mag_606w = data[UFD_NAMES[i]]['MAG_F606W']
        mag_814W = data[UFD_NAMES[i]]['MAG_F814W']
        color = mag_606w-mag_814W

        logging.info('Making scatter plot...')
        ax.scatter(color,mag_814w,1,color='k',label='A118 Member Stars')

        # check on DM and A
        logging.info('Plotting isochrones...')
        plot_one(iso,distance_modulus = 19.1,reddening = 0.02,ax=ax)

        ax.legend(loc='upper left',fontsize=18,scatterpoints=3)
        ax.set_xlim(-1,3)
        ax.set_ylim(28,16)
        ax.set_xticks(fontsize=18)
        ax.set_yticks(fontsize=18)
        ax.set_xlabel('F606W-F814W',fontsize=18)
        ax.set_ylabel('F814W',fontsize=18)

    plt.tight_layout()
    plt.savefig('cmd.pdf',dpi=500)
    plt.show()


