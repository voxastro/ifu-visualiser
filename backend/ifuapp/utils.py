import numpy as np


def npl(nparr, badmask=None):
    """
    Helper function to convert numpy arrays into list which needed for serialization.
    """
    if badmask is None:
        badmask = ~np.isfinite(nparr)
    return np.where(badmask, None, nparr).tolist()


def apply_search(queryset, search_query):
    """
    Function to make an arbitrarily queries. Applied to the main Cube table.
    """
    print("==================================================")
    print(search_query)
    print("==================================================")
    qs = queryset.extra(where=[search_query])
    return qs
