from astropy.table import Table
import numpy as np
from urllib.request import urlopen
import json
from tqdm import tqdm


def print2(string, file=None):
    print(string, file=file)
    print(string)


t = Table.read('sami_dr3.CubeObs.csv')

# avoid stellar cubes
mask = t['warnstar'] == 0

t_gal = t[mask]

# catid covers all dataproducts for the object even if target was observed twicely
sami_catids = np.unique(t_gal['catid'])

# extract corresponding data products dcID values for given catid
urls = [
    "https://datacentral.org.au/api/services/sov/?data_release__name=dr3&data_release__survey__name=sami&source_name=&page=1",
    "https://datacentral.org.au/api/services/sov/?data_release__name=dr3&data_release__survey__name=sami&source_name=&page=2",
    "https://datacentral.org.au/api/services/sov/?data_release__name=dr3&data_release__survey__name=sami&source_name=&page=3",
    "https://datacentral.org.au/api/services/sov/?data_release__name=dr3&data_release__survey__name=sami&source_name=&page=4",
    "https://datacentral.org.au/api/services/sov/?data_release__name=dr3&data_release__survey__name=sami&source_name=&page=5",
    "https://datacentral.org.au/api/services/sov/?data_release__name=dr3&data_release__survey__name=sami&source_name=&page=6",
    "https://datacentral.org.au/api/services/sov/?data_release__name=dr3&data_release__survey__name=sami&source_name=&page=7",
    "https://datacentral.org.au/api/services/sov/?data_release__name=dr3&data_release__survey__name=sami&source_name=&page=8",
    "https://datacentral.org.au/api/services/sov/?data_release__name=dr3&data_release__survey__name=sami&source_name=&page=9",
    "https://datacentral.org.au/api/services/sov/?data_release__name=dr3&data_release__survey__name=sami&source_name=&page=10",
    "https://datacentral.org.au/api/services/sov/?data_release__name=dr3&data_release__survey__name=sami&source_name=&page=11",
    "https://datacentral.org.au/api/services/sov/?data_release__name=dr3&data_release__survey__name=sami&source_name=&page=12",
    "https://datacentral.org.au/api/services/sov/?data_release__name=dr3&data_release__survey__name=sami&source_name=&page=13",
]

catids = np.array([])
ids = np.array([])

for url in urls:
    print(url)
    with urlopen(url) as response:
        data = json.loads(response.read())

    for d in data['results']:
        catids = np.append(catids, d['source_name'])
        ids = np.append(ids, d['id'])


_, idx1, idx2 = np.intersect1d(sami_catids, catids, return_indices=True)


# creale list of commands for downloading data products
with open('sami_dr3_download_commands.dat', 'w') as fileoutput:
    for catid, id in zip(sami_catids[idx1], ids[idx2]):
        url_download = f"https://datacentral.org.au/services/sov/{id}/download/"
        cmd = f"mkdir {catid}; wget {url_download} -O {catid}/{catid}.tgz; tar -zxvf {catid}/{catid}.tgz -C {catid}/; rm {catid}/{catid}.tgz"
        print2(cmd, fileoutput)
