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


def sort_points(coords, img, offset_istart=0, factor=10, test_plots=True):
    n_max = len(coords)
    # choose first point
    # select point which most distant to center of FoV
    istart = np.argmax(
        np.linalg.norm(coords - np.mean(coords, axis=0), axis=1)) + offset_istart

    new_coords = np.array([coords[istart, :]])
    indices = np.arange(n_max)
    new_indices = np.array([istart])

    n_cross_points = 1  # fake value to start

    while (len(new_coords) < n_max) & (n_cross_points != 0):

        # delta X, delta Y between last point in the new coords and rest of points in stack
        delta = coords - new_coords[-1]
        # one point before last
        delta2 = coords - new_coords[-2] if len(new_coords) >= 2 else delta

        distances = np.linalg.norm(delta, axis=1)
        # preselect points on the X and Y lines to avoid loops
        indices_crossed_pnts = np.where(
            (distances > 0) &
            ((abs(delta[:, 0]) < factor/2.0) | (abs(delta[:, 1]) < factor/2.0)))[0]
        n_cross_points = len(indices_crossed_pnts)

        # calculate phi
        phi = np.arctan2(delta[:, 0], delta[:, 1])
        # angle to have half-pixel in mid distance
        dphi = np.arctan2(factor/2.0, distances/2.0)

        delta_new1 = np.vstack((distances/2.0 * np.sin(phi-dphi),
                                distances/2.0 * np.cos(phi-dphi)))
        delta_new2 = np.vstack((distances/2.0 * np.sin(phi+dphi),
                                distances/2.0 * np.cos(phi+dphi)))

        coords_check1 = new_coords[-1] + delta_new1.T
        coords_check2 = new_coords[-1] + delta_new2.T

        # first calc mask for outlier points
        x1i = coords_check1[indices_crossed_pnts, 0].astype(int)
        y1i = coords_check1[indices_crossed_pnts, 1].astype(int)
        x2i = coords_check2[indices_crossed_pnts, 0].astype(int)
        y2i = coords_check2[indices_crossed_pnts, 1].astype(int)
        msk_out1 = (
            (x1i < 0) | (x1i > img.shape[0]) | (y1i < 0) | (y1i > img.shape[1])
        )
        msk_out2 = (
            (x2i < 0) | (x2i > img.shape[0]) | (y2i < 0) | (y2i > img.shape[1])
        )

        mask_right1sub = img[x1i[~msk_out1], y1i[~msk_out1]] == 0
        mask_right2sub = img[x2i[~msk_out2], y2i[~msk_out2]] == 1
        mask_right1 = ~msk_out1
        mask_right2 = ~msk_out2
        mask_right1[~msk_out1] = mask_right1sub
        mask_right2[~msk_out2] = mask_right2sub
        mask_right2[msk_out2] = True

        mask_right_points = mask_right1 & mask_right2

        if test_plots:
            fig = plt.figure(figsize=(12, 12))
            plt.imshow(img, origin='lower')
            plt.plot(coords[:, 1], coords[:, 0], '+')

            plt.plot(new_coords[-1, 1], new_coords[-1, 0],
                     'o', ms=3, color='orange')
            plt.plot(coords[indices_crossed_pnts, 1].astype(int),
                     coords[indices_crossed_pnts, 0].astype(int), '+')

        indices_good_points = indices_crossed_pnts[mask_right_points]
        inew = np.argmin(distances[indices_good_points])
        inew = indices_good_points[inew]

        if (new_indices[-1] in new_indices[:-1]) & (inew in new_indices):
            print("loop detected")
            indices_good_points_no_loop = indices_good_points[indices_good_points != inew]
            if len(indices_good_points_no_loop) == 0:
                # in this case not more points but some internal bad spaxels are exist
                break
            inew = np.argmin(distances[indices_good_points_no_loop])
            inew = indices_good_points_no_loop[inew]

        if test_plots:
            for cc, ck1, ck2 in zip(
                coords[indices_crossed_pnts[mask_right_points]],
                coords_check1[indices_crossed_pnts[mask_right_points]],
                coords_check2[indices_crossed_pnts[mask_right_points]]
            ):
                plt.plot([new_coords[-1, 1], ck1[1], cc[1]],
                         [new_coords[-1, 0], ck1[0], cc[0]], '-o')
                plt.plot([new_coords[-1, 1], ck2[1], cc[1]],
                         [new_coords[-1, 0], ck2[0], cc[0]], '-o')

            plt.plot(coords[inew, 1], coords[inew, 0],
                     '+', ms=10, mew=3, color='red')

            plt.pause(0.02)
            plt.close()

        new_coords = np.append(new_coords, [coords[inew]], axis=0)
        new_indices = np.append(new_indices, inew)
        # plt.text(coords[ipoint, 1], coords[ipoint, 0], len(new_coords))

    return new_coords


def detect_edges(img, factor=10, npix_reduction=5,
                 threshold_rel=0.5, window_size=13, plot=False):
    new_shape = (img.shape[0]*factor, img.shape[1]*factor)
    img_hr = transform.resize(img, new_shape, order=0)
    img_hr[img_hr != 0] = 1

    img_enchanced = feature.corner_shi_tomasi(img_hr)
    crds = feature.corner_peaks(img_enchanced, threshold_rel=threshold_rel,
                                min_distance=factor-npix_reduction,
                                exclude_border=False)
    crds_subpix = feature.corner_subpix(img_hr, crds, window_size=window_size)
    badmask = ~np.isfinite(crds_subpix)
    crds_subpix[badmask] = crds[badmask]

    # now exclude corners
    msk_corners = ((np.linalg.norm(crds_subpix - [0, 0], axis=1) < factor/2.0) |
                   (np.linalg.norm(crds_subpix - [new_shape[0], 0], axis=1) < factor/2.0) |
                   (np.linalg.norm(crds_subpix - [new_shape[0], new_shape[1]], axis=1) < factor/2.0) |
                   (np.linalg.norm(crds_subpix - [0, new_shape[1]], axis=1) < factor/2.0))
    crds_subpix = crds_subpix[~msk_corners]

    if plot:
        fig = plt.figure(figsize=(15, 7))
        ax1 = plt.subplot(1, 1, 1)
        # ax2 = plt.subplot(1, 2, 2)

        # ax1.imshow(img_hr)
        ax1.imshow(img_enchanced)

        ax1.plot(crds[:, 1], crds[:, 0], '+', color='lightblue', lw=4)
        ax1.plot(crds_subpix[:, 1], crds_subpix[:, 0],
                 '+', color='red', mew=3, ms=6)
        plt.show()

    crds_subpix = sort_points(
        crds_subpix, img_hr, factor=factor, test_plots=False)

    return crds_subpix / factor


def skycoords_to_str(coords):
    s = "{" + \
        ",".join(
            [f"{'{'}{c.ra.deg:.6f},{c.dec.deg:.6f}{'}'}" for c in coords]) + "}"
    return s


def hdr2fov(w, naxis1, naxis2):
    px_x = np.array([0, 0, naxis1, naxis1]) - 0.5
    px_y = np.array([0, naxis2, naxis2, 0]) - 0.5
    return wutils.pixel_to_skycoord(px_x, px_y, w)


def process_file(job, testplot=False):
    f = job[0]
    q = job[1]
    print(q, f)
    hdr = fits.getheader(f)
    file_noext = os.path.basename(f).split('.fits')[0]

    if 'manga' in f:
        hdr1 = fits.getheader(f, 1)
        w = WCS(hdr1).dropaxis(-1)
        coords = hdr2fov(w, hdr1['NAXIS1'], hdr1['NAXIS2'])
        # coordinated of FITS file corners
        fov_fits = skycoords_to_str(coords)

        fovs = dict(manga19=dict(x=[3.5, 6.0, 3.5, -3.5, -6.0, -3.5, 3.5],
                                 y=[5.33, 0.0, -5.33, -5.33, 0.0, 5.33, 5.33]),
                    manga37=dict(x=[4.8, 8.5, 4.8, -4.8, -8.5, -4.8, 4.8],
                                 y=[7.5, 0.0, -7.5, -7.5, 0.0, 7.5, 7.5]),
                    manga61=dict(x=[6.0, 11.0, 6.0, -6.0, -11.0, -6.0, 6.0],
                                 y=[9.5, 0.0, -9.5, -9.5, 0.0, 9.5, 9.5]),
                    manga91=dict(x=[7.35, 13.6, 7.35, -7.35, -13.6, -7.35, 7.35],
                                 y=[11.8, 0.0, -11.8, -11.8, 0.0, 11.8, 11.8]),
                    manga127=dict(x=[8.57, 16.11, 8.57, -8.57, -16.1, -8.57, 8.57],
                                  y=[14.0, 0.0, -14.0, -14.0, 0.0, 14.0, 14.0]))
        # MaNGA FoV
        plateifu = hdr['PLATEIFU']
        plate, ifudsg = plateifu.split('-')
        fov = fovs[f"manga{ifudsg[:-2]}"]
        manga_fov_coords = SkyCoord(
            hdr['IFURA'] + np.array(fov['x']) / 3600.0 /
            np.cos(np.deg2rad(hdr['IFUDEC'])),
            hdr['IFUDEC'] + np.array(fov['y']) / 3600.0,
            unit=(u.deg, u.deg)
        )

        manga_fov_str = skycoords_to_str(manga_fov_coords)

        ivar = fits.getdata(f, 'IVAR')
        imgmsk = np.nansum(ivar, axis=0)
        msk = imgmsk != 0
        imgmsk[msk] = 0
        imgmsk[~msk] = 1

        c_pix = detect_edges(imgmsk, plot=False) - 0.45
        coords_edges = wutils.pixel_to_skycoord(c_pix[:, 1], c_pix[:, 0], w)

        manga_fov_str = skycoords_to_str(coords_edges)

        row = (q+1, hdr['IFURA'], hdr['IFUDEC'], 'manga',
               file_noext, hdr['EXPTIME'], hdr['MANGAID'], hdr['PLATEIFU'],
               '', '', '', '',
                   '', '', fov_fits, manga_fov_str)
    elif 'sami' in f:
        w = WCS(hdr).dropaxis(-1)
        coords = hdr2fov(w, hdr['NAXIS1'], hdr['NAXIS2'])
        fov_fits = skycoords_to_str(coords)

        var = fits.getdata(f, 'VARIANCE')
        imgmsk = np.nansum(var, axis=0)
        msk = imgmsk != 0
        imgmsk[msk] = 0
        imgmsk[~msk] = 1

        c_pix = detect_edges(imgmsk, plot=False) - 0.45
        coords_edges = wutils.pixel_to_skycoord(c_pix[:, 1], c_pix[:, 0], w)
        fov_str = skycoords_to_str(coords_edges)

        center = w.pixel_to_world(hdr['NAXIS1']/2.0, hdr['NAXIS2']/2.0)
        cube = file_noext.split(hdr['NAME']+'_')[1]
        catid, seqnum = file_noext.split('_')[:2]
        cubeidpub = f"{catid}_{seqnum}"

        row = (q+1, center.ra.deg, center.dec.deg, 'sami',
               file_noext, hdr['TOTALEXP'], '', '',
               catid, cubeidpub, '', '',
               '', '', fov_fits, fov_str)

    elif 'califa' in f:
        w = WCS(hdr).dropaxis(-1)

        coords = hdr2fov(w, hdr['NAXIS1'], hdr['NAXIS2'])
        fov_fits = skycoords_to_str(coords)

        fibcov = fits.getdata(f, 'FIBCOVER')
        imgmsk = np.nansum(fibcov, axis=0)
        msk = imgmsk != 0
        imgmsk[msk] = 0
        imgmsk[~msk] = 1

        c_pix = detect_edges(imgmsk, plot=False, factor=10,
                             npix_reduction=4) - 0.45
        coords_edges = wutils.pixel_to_skycoord(c_pix[:, 1], c_pix[:, 0], w)
        fov_str = skycoords_to_str(coords_edges)

        center = w.pixel_to_world(hdr['NAXIS1']/2.0, hdr['NAXIS2']/2.0)
        row = (q+1, center.ra.deg, center.dec.deg, 'califa',
               file_noext, 900*3, '', '',
               '', '', f"{hdr['CALIFAID']}", file_noext.split('.')[0],
               file_noext.split('.')[1], '', fov_fits, fov_str)

    elif 'atlas' in f:

        scale = 0.8
        hdr = fits.getheader(f)
        tab = fits.getdata(f, 2)

        pix_x = np.round(tab['A'] / scale).astype(int)
        pix_y = np.round(tab['D'] / scale).astype(int)
        nx = np.round(np.max(pix_x) - np.min(pix_x)+1).astype(int)
        ny = np.round(np.max(pix_y) - np.min(pix_y)+1).astype(int)
        sz = [ny, nx]
        imsk = np.full(sz, np.nan)

        imsk[-np.min(pix_y) + pix_y,
             -np.min(pix_x) + pix_x] = np.arange(len(pix_x))

        ind_center = np.argwhere((pix_x == 0) & (pix_y == 0))[0][0]
        w = WCS(naxis=2)
        w.wcs.crpix = [-np.min(pix_y) + pix_y[ind_center],
                       -np.min(pix_x) + pix_x[ind_center]]

        w.wcs.crval = [hdr['TCRVL6'], hdr['TCRVL7']]
        w.wcs.ctype = ['RA---TAN', 'DEC--TAN']
        w.wcs.cdelt = [-scale/3600.0, scale/3600.0]

        coords = hdr2fov(w, sz[1], sz[0])

        imgmsk = imsk.copy()
        msk = np.isfinite(imgmsk)
        imgmsk[msk] = 0
        imgmsk[~msk] = 1

        c_pix = detect_edges(imgmsk, plot=False, factor=10,
                             npix_reduction=4) - 0.45
        coords_edges = wutils.pixel_to_skycoord(c_pix[:, 1], c_pix[:, 0], w)
        fov_str = skycoords_to_str(coords_edges)

        # fits.PrimaryHDU(data=imsk, header=w.to_header()
        #                 ).writeto('tmp.fits', overwrite=True)

        row = (q+1, hdr['TCRVL6'], hdr['TCRVL7'], 'atlas3d',
               file_noext, None, '', '',
               '', '', '', '',
               '', file_noext.split('_')[1], '', fov_str)

    # test plots
    if testplot:
        plt.close()
        fig = plt.figure(figsize=(15, 13))
        ax = fig.add_subplot(projection=w)
        ax.imshow(imgmsk)
        ax.plot(coords.ra.deg, coords.dec.deg,
                transform=ax.get_transform('world'))
        ax.plot(coords_edges.ra.deg, coords_edges.dec.deg, lw=3, ls='--',
                transform=ax.get_transform('world'))

        for i, crd in enumerate(coords_edges):
            ax.text(crd.ra.deg, crd.dec.deg, str(i),
                    transform=ax.get_transform('world'))

        plt.pause(0.01)

    return row


if __name__ == '__main__':

    # for test run
    # path_manga = "/data/manga_dr16/spectro/redux/v2_4_3/9506//stack/manga-*-LOGCUBE.fit*"
    # path_sami = "/data/sami_dr3/98880/*_cube_blue.fits*"
    path_data = "/data"
    # path_data = "/Users/ik52/obs/ifu-visualiser-data"
    ofile = 'table_cubes_test.csv'

    path_manga = f"{path_data}/manga_dr17/spectro/redux/MPL-11/*/stack/manga-*-LOGCUBE.fit*"
    path_sami = f"{path_data}/sami_dr3/*/*_cube_blue.fits*"
    path_califa = f"{path_data}/califa_dr3/*/reduced_v2.2/*rscube.fits*"
    path_atlas = f"{path_data}/atlas3d/MS_*.fits"

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
                     'califa_cube', 'atlas_name', 'fov_fits', 'fov_ifu'),
              dtype=(np.int32, np.float32, np.float32, 'U100',
                     'U100', np.float32, 'U100', 'U100',
                     'U100', 'U100', 'U100', 'U100',
                     'U100', 'U100', 'U200', 'U20000'))

    files = files_manga + files_sami + files_califa #+ files_atlas

    jobs = [[f, q] for q, f in enumerate(files)]

    with Pool(5) as p:
        rows = p.map(process_file, jobs)

    for row in tqdm(rows):
        t.add_row(row)

    t.write(ofile, overwrite=True)
