"""
Collect information for the main table Cubes
"""
from glob import glob
from astropy.table import Table
from astropy.io import fits
from astropy.wcs import WCS, utils as wutils
from astropy.coordinates import SkyCoord
import astropy.units as u
import numpy as np
import os
from tqdm import tqdm
from astropy.wcs import FITSFixedWarning
from skimage import feature
from skimage import transform

import matplotlib.pyplot as plt
from multiprocessing import Pool

import warnings
warnings.simplefilter('ignore', category=FITSFixedWarning)


def find_direction(datamask, current_position, avoid_direction=None):
    """Function to check direction and get coords of the next point"""
    # Left pixel should be 1 (not data) and right one 0 (data).
    # Such definition correspond to clock-wise direction of go round

    x0 = current_position[0]
    y0 = current_position[1]

    # UP
    is_data_left = datamask[int(y0 + 0.5), int(x0 - 0.5)]
    is_data_right = datamask[int(y0 + 0.5), int(x0 + 0.5)]
    if (is_data_left == False) & (is_data_right == True):
        return 'U', [x0, y0 + 1]

    # LEFT
    is_data_left = datamask[int(y0 - 0.5), int(x0 - 0.5)]
    is_data_right = datamask[int(y0 + 0.5), int(x0 - 0.5)]
    if (is_data_left == False) & (is_data_right == True):
        return 'L', [x0 - 1, y0]

    # DOWN
    is_data_left = datamask[int(y0 - 0.5), int(x0 + 0.5)]
    is_data_right = datamask[int(y0 - 0.5), int(x0 - 0.5)]
    if (is_data_left == False) & (is_data_right == True):
        return 'D', [x0, y0 - 1]

    # RIGHT
    is_data_left = datamask[int(y0 + 0.5), int(x0 + 0.5)]
    is_data_right = datamask[int(y0 - 0.5), int(x0 + 0.5)]
    if (is_data_left == False) & (is_data_right == True):
        return 'R', [x0 + 1, y0]

    raise Exception("Fucking error")


def detect_edges2(datamask, factor=10, npix_reduction=5, threshold_rel=0.5, window_size=13, plot=False):

    # add extra pixel as an overframe
    imgp = np.pad(datamask, 1, constant_values=False)

    # find most distant element of the Field-of-View
    x = np.arange(imgp.shape[0])
    y = np.arange(imgp.shape[1])
    xx, yy = np.meshgrid(y, x)
    dist = np.sqrt(xx**2 + yy**2)

    idx_max = np.argmin(dist[imgp])

    start_x = xx[imgp][idx_max] - 0.5 # -0.5 to put points in the corner of the pixel
    start_y = yy[imgp][idx_max] - 0.5

    # initial point in the list of vertices
    coords = [[start_x, start_y]]
        
    reach_initial_point = False
    current_direction = None
    current_coord = coords[0]

    while reach_initial_point != True:
        new_direction, new_coord = find_direction(imgp, current_coord)
            
        if (new_direction != current_direction) & (current_direction is not None):            
            # check case of loop, when single spaxel can cause loop
            is_loop_detected = current_coord in coords
            coords.append(current_coord)
            if is_loop_detected:
                # loop detected, so need to change direction to opposite
                if new_direction == 'U':
                    new_direction = 'D'
                    new_coord = [new_coord[0], new_coord[1]-2]
                elif new_direction == 'L':
                    new_direction = 'R'
                    new_coord = [new_coord[0]+2, new_coord[1]]
                elif new_direction == 'D':
                    new_direction = 'U'
                    new_coord = [new_coord[0], new_coord[1]+2]
                elif new_direction == 'R':
                    new_direction = 'L'
                    new_coord = [new_coord[0]-2, new_coord[1]]
                else:
                    raise Exception("Error in the loop detection block")

        # update current values
        current_coord = new_coord
        current_direction = new_direction
        reach_initial_point = new_coord == coords[0]


    coords.append(coords[0]) # to complete the loop
    coords = np.array(coords)
    
    if plot:
        plt.figure(figsize=(10, 10))
        plt.tight_layout()
        plt.imshow(datamask, origin='lower')
        plt.plot(coords[:, 0], coords[:, 1], marker='.', color='red')
        plt.show()    
    
    # unity takes into account padding of one spaxel
    return coords - 1


def skycoords_to_str(coords):
    s = "{" + \
        ",".join(
            [f"{'{'}{c.ra.deg:.6f},{c.dec.deg:.6f}{'}'}" for c in coords]) + "}"
    return s


def hdr2fov(w, naxis1, naxis2):
    px_x = np.array([0, 0, naxis1, naxis1]) - 0.5
    px_y = np.array([0, naxis2, naxis2, 0]) - 0.5
    px_x = np.append(px_x, px_x[0])
    px_y = np.append(px_y, px_y[0])
    return wutils.pixel_to_skycoord(px_x, px_y, w)


def process_file(job, testplot=False):
    f = job[0]
    q = job[1]

    hdr = fits.getheader(f)
    file_noext = os.path.basename(f).split('.fits')[0]

    if 'manga_dr17' in f:
        hdr1 = fits.getheader(f, 1)
        w = WCS(hdr1).dropaxis(-1)
        coords = hdr2fov(w, hdr1['NAXIS1'], hdr1['NAXIS2'])
        # coordinated of FITS file corners
        fov_fits = skycoords_to_str(coords)

        ivar = fits.getdata(f, 'IVAR')
        image_mask = np.nansum(ivar, axis=0).astype(bool)

        c_pix = detect_edges2(image_mask)
        coords_edges = wutils.pixel_to_skycoord(c_pix[:, 0], c_pix[:, 1], w)
        fov_str = skycoords_to_str(coords_edges)

        row = (q+1, hdr['IFURA'], hdr['IFUDEC'], 'manga', file_noext, hdr['EXPTIME'],
               hdr['MANGAID'], hdr['PLATEIFU'],
               '', '',
               '', '', '',
               '',
               '', '',
               fov_fits, fov_str)

    elif 'sami_dr3' in f:

        w = WCS(hdr).dropaxis(-1)
        coords = hdr2fov(w, hdr['NAXIS1'], hdr['NAXIS2'])
        fov_fits = skycoords_to_str(coords)

        var = fits.getdata(f, 'VARIANCE')
        image_mask = np.nansum(var, axis=0).astype(bool)
       
        c_pix = detect_edges2(image_mask)
        coords_edges = wutils.pixel_to_skycoord(c_pix[:, 0], c_pix[:, 1], w)
        fov_str = skycoords_to_str(coords_edges)

        center = w.pixel_to_world(hdr['NAXIS1']/2.0, hdr['NAXIS2']/2.0)
        cube = file_noext.split(hdr['NAME']+'_')[1]
        catid, seqnum = file_noext.split('_')[:2]
        cubeidpub = f"{catid}_{seqnum}"

        row = (q+1, center.ra.deg, center.dec.deg, 'sami', file_noext, hdr['TOTALEXP'],
               '', '',
               catid, cubeidpub,
               '', '', '',
               '',
               '', '',
               fov_fits, fov_str)

    elif 'califa_dr3' in f:
        w = WCS(hdr).dropaxis(-1)

        coords = hdr2fov(w, hdr['NAXIS1'], hdr['NAXIS2'])
        fov_fits = skycoords_to_str(coords)

        fibcov = fits.getdata(f, 'FIBCOVER')
        image_mask = np.nansum(fibcov, axis=0).astype(bool)
        
        c_pix = detect_edges2(image_mask)
        coords_edges = wutils.pixel_to_skycoord(c_pix[:, 0], c_pix[:, 1], w)
        fov_str = skycoords_to_str(coords_edges)

        center = w.pixel_to_world(hdr['NAXIS1']/2.0, hdr['NAXIS2']/2.0)
        row = (q+1, center.ra.deg, center.dec.deg, 'califa', file_noext, 900*3,
               '', '',
               '', '',
               f"{hdr['CALIFAID']}", file_noext.split('.')[0], file_noext.split('.')[1],
               '',
               '', '',
               fov_fits, fov_str)

    elif 'atlas3d' in f:
        # https://www-astro.physics.ox.ac.uk/atlas3d/
        scale = 1.0
        hdr = fits.getheader(f)
        tab = fits.getdata(f, 2)

        pix_x = np.round(tab['A'] / scale).astype(int)
        pix_y = np.round(tab['D'] / scale).astype(int)
        nx = np.round(np.max(pix_x) - np.min(pix_x)+1).astype(int)
        ny = np.round(np.max(pix_y) - np.min(pix_y)+1).astype(int)
        sz = [ny, nx]
        image_mask = np.full(sz, False)
        image_mask[-np.min(pix_y) + pix_y, -np.min(pix_x) + pix_x] = True

        w = WCS(naxis=2)
        w.wcs.crpix = [-np.min(pix_y), -np.min(pix_x)]
        w.wcs.crval = [hdr['TCRVL6'], hdr['TCRVL7']]
        w.wcs.ctype = ['RA---TAN', 'DEC--TAN']
        w.wcs.cdelt = [-scale/3600.0, scale/3600.0]

        coords = hdr2fov(w, sz[1], sz[0])

        c_pix = detect_edges2(image_mask)
        coords_edges = wutils.pixel_to_skycoord(c_pix[:, 0], c_pix[:, 1], w)
        fov_str = skycoords_to_str(coords_edges)

        row = (q+1, hdr['TCRVL6'], hdr['TCRVL7'], 'atlas3d', file_noext, None,
               '', '',
               '', '',
               '', '', '',
               file_noext.split('_')[1],
               '', '',
               '', fov_str)

    elif 'Binospec_IFU' in f:
        hdr1 = fits.getheader(f, 'IFU_CUBE')
        w = WCS(hdr1).dropaxis(-1)
        coords = hdr2fov(w, hdr1['NAXIS1'], hdr1['NAXIS2'])
        coords_edges = coords
        fov_fits = skycoords_to_str(coords)
        center = w.pixel_to_world(hdr1['NAXIS1']/2.0, hdr1['NAXIS2']/2.0)

        fragment = file_noext.replace('bino_ifu_', '').replace('_abs_cube_lin', '')
        fragment_splitted = fragment.split('_')
        bino_grating = fragment_splitted[-1]
        bino_name = fragment.replace('_'+bino_grating, '')

        row = (q+1, center.ra.deg, center.dec.deg, 'bino', file_noext, hdr1['EXPTIME'],
               '', '',
               '', '',
               '', '', '',
               '',
               bino_name, bino_grating,
               fov_fits, '')

    # test plots
    if testplot:
        plt.close()
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(projection=w)
        # ax.imshow(imgmsk)
        ax.plot(coords.ra.deg, coords.dec.deg, transform=ax.get_transform('world'))
        ax.plot(coords_edges.ra.deg, coords_edges.dec.deg, lw=2, ls='-', marker='.',
                transform=ax.get_transform('world'))

        for i, crd in enumerate(coords_edges):
            ax.text(crd.ra.deg, crd.dec.deg, str(i), ha='center', fontsize=9, color='C1',
                    transform=ax.get_transform('world'))

        plt.pause(0.001)

    return row


if __name__ == '__main__':

    # path within the Docker container
    path_data = "/data"
    # path on laptop
    #path_data = "/Users/ik52/obs/ifu-visualiser-data"
    ofile = 'table_cubes_test.csv'

    path_manga = f"{path_data}/manga_dr17/spectro/redux/MPL-11/*/stack/manga-*-LOGCUBE.fit*"
    path_sami = f"{path_data}/sami_dr3/*/*_cube_blue.fits*"
    path_califa = f"{path_data}/califa_dr3/*/reduced_v2.2/*rscube.fits*"
    path_atlas = f"{path_data}/atlas3d/MS_*.fits"
    path_bino = f"{path_data}/Binospec_IFU/bino_ifu_*_cube_lin.fits"

    print("Searching MaNGA files...")
    files_manga = glob(path_manga)

    print("Searching SAMI files...")
    files_sami = glob(path_sami)

    print("Searching CALIFA files...")
    files_califa = glob(path_califa)

    print("Searching ATLAS files...")
    files_atlas = glob(path_atlas)
    
    print("Searching Bino files...")
    files_bino = glob(path_bino)

    print(f"MaNGA: {len(files_manga)} files")
    print(f"SAMI: {len(files_sami)} files")
    print(f"Califa: {len(files_califa)} files")
    print(f"Atlas3D: {len(files_atlas)} files")
    print(f"Bino-IFU: {len(files_bino)} files")

    t = Table(names=('id', 'ra', 'dec', 'survey', 'filename', 'exptime',
                     'manga_id', 'manga_plateifu',
                     'sami_catid', 'sami_cubeidpub',
                     'califa_id', 'califa_name', 'califa_cube',
                     'atlas_name',
                     'bino_name', 'bino_grating',
                     'fov_fits', 'fov_ifu'),
              dtype=(np.int32, np.float32, np.float32, 'U100', 'U100', np.float32, # general
                     'U100', 'U100', # manga
                     'U100', 'U100', # sami
                     'U100', 'U100', 'U100', # califa
                     'U100', #atlas
                     'U100', 'U100', # bino 
                     'U200', 'U20000'))

    files = files_manga + files_sami + files_califa + files_atlas + files_bino

    jobs = [[f, q] for q, f in enumerate(files)]

    multiproc = True

    if multiproc:
        with Pool(3) as p:
            rows = p.map(process_file, jobs)
    else:
        # useful mostly for debug purpose
        rows = map(process_file, jobs)

    for row in tqdm(rows):
        t.add_row(row)

    t.write(ofile, overwrite=True)
