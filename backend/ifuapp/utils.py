import numpy as np

def npl(nparr, badmask=None):
    """
    Helper function to convert numpy arrays into list which needed for serialization.
    """
    if badmask is None:
        badmask = ~np.isfinite(nparr)
    return np.where(badmask, None, nparr).tolist()
