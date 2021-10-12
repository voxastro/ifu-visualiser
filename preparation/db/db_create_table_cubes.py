"""
Collect information for the main table Cubes
"""
from glob import glob
from astropy.table import Table
from astropy.io import fits
from astropy.wcs import WCS, utils as wutils
import numpy as np
import os
from tqdm import tqdm

path_manga = "/data/manga_dr16/spectro/redux/v2_4_3/*/stack/manga-*-LOGCUBE.fit*"
path_sami = "/data/sami_dr3/*/*_cube_blue.fits*"
# path_manga = "/data/manga_dr16/spectro/redux/v2_4_3/9506//stack/manga-*-LOGCUBE.fit*"
# path_sami = "/data/sami_dr3/98880/*_cube_blue.fits*"
path_califa = "/data/califa_dr3/*/reduced_v2.2/*rscube.fits*"
path_atlas = "/data/atlas3d/MS_*.fits"

print("Searching MaNGA files...")
files_manga = glob(path_manga)

print("Searching SAMI files...")
files_sami = glob(path_sami)

print("Searching CALIFA files...")
files_califa = glob(path_califa)

print("Searching ATLAS files...")
files_atlas = glob(path_atlas)

print(f"MaNGA: {len(files_manga)} files")
print(f"SAMI: {len(files_sami)} files")
print(f"Califa: {len(files_califa)} files")
print(f"Atlas3D: {len(files_atlas)} files")

t = Table(names=('id', 'ra', 'dec', 'survey',
                 'filename', 'exptime', 'manga_id', 'manga_plateifu',
                 'sami_catid', 'sami_cubeidpub', 'califa_id', 'califa_name',
                 'califa_cube', 'atlas_name', 'fov_fits'),
          dtype=(np.int32, np.float32, np.float32, 'U100',
                 'U100', np.float32, 'U100', 'U100',
                 'U100', 'U100', 'U100', 'U100',
                 'U100', 'U100', 'U150'))

for q, f in enumerate(tqdm(files_manga + files_sami + files_califa + files_atlas)):
# for q, f in enumerate(tqdm(files_manga[:100] + files_sami[:100] + files_califa[:100] + files_atlas[:100])):

    hdr = fits.getheader(f)
    file_noext = os.path.basename(f).split('.fits')[0]

    if 'manga' in f:
        hdr1 = fits.getheader(f, 1)
        w = WCS(hdr1).dropaxis(-1)
        coords = wutils.pixel_to_skycoord(
            [0, 0, hdr1['NAXIS1'], hdr1['NAXIS1']],
            [0, hdr1['NAXIS2'], hdr1['NAXIS2'], 0], w)

        fov_fits = "{" + ",".join([f"{'{'}{c.ra.deg:.6f},{c.dec.deg:.6f}{'}'}" for c in coords]) + "}"
        t.add_row((q+1, hdr['IFURA'], hdr['IFUDEC'], 'manga',
                   file_noext, hdr['EXPTIME'], hdr['MANGAID'], hdr['PLATEIFU'],
                   '', '', '', '',
                   '', '', fov_fits))
    elif 'sami' in f:
        w = WCS(hdr).dropaxis(-1)

        coords = wutils.pixel_to_skycoord(
            [0, 0, hdr['NAXIS1'], hdr['NAXIS1']],
            [0, hdr['NAXIS2'], hdr['NAXIS2'], 0], w)

        fov_fits = "{" + ",".join([f"{'{'}{c.ra.deg:.6f},{c.dec.deg:.6f}{'}'}" for c in coords]) + "}"
    
        center = w.pixel_to_world(hdr['NAXIS1']/2.0, hdr['NAXIS2']/2.0)
        cube = file_noext.split(hdr['NAME']+'_')[1]
        catid, seqnum = file_noext.split('_')[:2]
        cubeidpub = f"{catid}_{seqnum}"
        t.add_row((q+1, center.ra.deg, center.dec.deg, 'sami',
                   file_noext, hdr['TOTALEXP'], '', '',
                   catid, cubeidpub, '', '',
                   '', '', fov_fits))

    elif 'califa' in f:
        w = WCS(hdr).dropaxis(-1)

        coords = wutils.pixel_to_skycoord(
            [0, 0, hdr['NAXIS1'], hdr['NAXIS1']],
            [0, hdr['NAXIS2'], hdr['NAXIS2'], 0], w)

        fov_fits = "{" + ",".join([f"{'{'}{c.ra.deg:.6f},{c.dec.deg:.6f}{'}'}" for c in coords]) + "}"

        center = w.pixel_to_world(hdr['NAXIS1']/2.0, hdr['NAXIS2']/2.0)
        t.add_row((q+1, center.ra.deg, center.dec.deg, 'califa',
                   file_noext, 900*3, '', '',
                   '', '', f"{hdr['CALIFAID']}", file_noext.split('.')[0],
                   file_noext.split('.')[1], '', fov_fits))
    elif 'atlas' in f:
        t.add_row((q+1, hdr['TCRVL6'], hdr['TCRVL7'], 'atlas3d',
                   file_noext, None, '', '',
                   '', '', '', '',
                   '', file_noext.split('_')[1], ''))


t.write('table_cubes.csv', overwrite=True)
