"""
Collect information for the main table Cubes
"""
from glob import glob
from astropy.table import Table
from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
import os
from tqdm import tqdm

print("Searching MaNGA files...")
files_manga = glob(
    "/sdss16/manga/spectro/redux/v2_4_3/*/stack/manga-*-LOGCUBE.fits*")
print("Searching SAMI files...")
files_sami = glob("/db5/Data/sami_dr3/*/*_cube_*.fits*")
print("Searching CALIFA files...")
files_califa = glob(
    "/db5/Data/califa_dr3/*/reduced_v2.2/*rscube.fits*")
print("Searching ATLAS files...")
files_atlas = glob("/db5/Data/atlas3d/MS_*.fits")

print(f"MaNGA: {len(files_manga)} files")
print(f"SAMI: {len(files_sami)} files")
print(f"Califa: {len(files_califa)} files")
print(f"Atlas3D: {len(files_atlas)} files")

t = Table(names=('id', 'ra', 'dec', 'survey', 'filename', 'exptime', 'manga_id', 'manga_plateifu',
                 'sami_catid', 'sami_cube', 'califa_id', 'califa_name', 'califa_cube', 'atlas_name'),
          dtype=(np.int32, np.float32, np.float32, 'U100', 'U100', np.float32, 'U100', 'U100', 'U100', 'U100', 'U100', 'U100', 'U100', 'U100'))


for q, f in enumerate(tqdm(files_manga + files_sami + files_califa + files_atlas)):

    hdr = fits.getheader(f)
    file_noext = os.path.basename(f).split('.fits')[0]

    if 'sdss16' in f:
        t.add_row((q+1, hdr['IFURA'], hdr['IFUDEC'], 'manga', file_noext,
                  hdr['EXPTIME'], hdr['MANGAID'], hdr['PLATEIFU'], '', '', '', '', '', ''))
    elif 'sami' in f:
        w = WCS(hdr).dropaxis(-1)
        center = w.pixel_to_world(hdr['NAXIS1']/2.0, hdr['NAXIS2']/2.0)
        cube = file_noext.split(hdr['NAME']+'_')[1]
        t.add_row((q+1, center.ra.deg, center.dec.deg, 'sami', file_noext,
                  hdr['TOTALEXP'], '', '', hdr['NAME'], cube, '', '', '', ''))
    elif 'califa' in f:
        w = WCS(hdr).dropaxis(-1)
        center = w.pixel_to_world(hdr['NAXIS1']/2.0, hdr['NAXIS2']/2.0)
        t.add_row((q+1, center.ra.deg, center.dec.deg, 'califa', file_noext,
                  900*3, '', '', '', '', hdr['CALIFAID'], hdr['OBJECT'], file_noext.split('.')[1], ''))
    elif 'atlas' in f:
        t.add_row((q+1, hdr['TCRVL6'], hdr['TCRVL7'], 'atlas3d', file_noext,
                  None, '', '', '', '', '', '', '', file_noext.split('_')[1]))

t.write('table_cubes.csv', overwrite=True)
