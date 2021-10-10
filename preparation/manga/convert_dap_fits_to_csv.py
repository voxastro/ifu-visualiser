from astropy.table import Table
import numpy as np
from tqdm import tqdm


def print2(text, file=None, onlyfile=False):
    if not onlyfile:
        print(text)
    if file is not None:
        print(text, file=file)


filein = 'dapall-v2_4_3-2.2.1.fits'
fileout = 'dapall-v2_4_3-2.2.1.csv'

table = Table.read(filein, hdu='MANGA')

with open(fileout, 'w') as f:
    nm = ''
    for ir, r in tqdm(enumerate(table)):
        st = ''
        for v, n in zip(r, r.keys()):
            if isinstance(v, np.ma.core.MaskedConstant):
                if v.mask:
                    st += ','
                    nm += ','
                else:
                    st += v.astype(str) + ','
                    nm += n + ','
            elif isinstance(v, np.ndarray):
                st += ','.join([element.astype(str) for element in v]) + ','
                nm += ','.join([n+'_'+flt for element, flt in zip(v,
                               ['f', 'n', 'u', 'g', 'r', 'i', 'z'])]) + ','
            elif isinstance(v, str):
                st += v + ','
                nm += n + ','
            else:
                st += v.astype(str) + ','
                nm += n + ','

        if ir == 0:
            print2(nm[:-1], file=f, onlyfile=True)

        print2(st[:-1], file=f, onlyfile=True)
