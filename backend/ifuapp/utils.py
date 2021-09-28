from django.db.models.lookups import Lookup
import numpy as np
from customquery import Parser
from django.db.models import F, Func, Value, BooleanField, FloatField
from rest_framework import exceptions


def npl(nparr, badmask=None):
    """
    Helper function to convert numpy arrays into list which needed for serialization.
    """
    if badmask is None:
        badmask = ~np.isfinite(nparr)
    return np.where(badmask, None, nparr).tolist()


class RadialQuery(Func):
    function = 'q3c_radial_query'
    output_field = BooleanField()


class Distance(Func):
    function = 'q3c_dist'
    output_field = FloatField()



def apply_search(queryset, search_query):
    parser = Parser(queryset.model)
    
    try:
        filter = parser.parse(search_query)
    except:
        raise exceptions.ParseError(detail='Bad query string.')

    # check how many Cone statements are in the search query
    n_cones = len(parser.extra_params['cones'])

    if n_cones > 0:
        # if there is a Cone statement we have to add annotated field(s)
        # cone_dist (cone_dist1, cone_dist2, etc)
        kws_query = dict()
        kws_dist = dict()
        for q in range(n_cones):
            idx_str = "" if q == 0 else str(q)
            c = parser.extra_params['cones'][q]
            ra = Value(c['cone_ra'])
            dec = Value(c['cone_dec'])
            radius = Value(c['cone_radius'])

            kws_query[f"cone_query{idx_str}"] = RadialQuery(F('ra'), F('dec'), ra, dec, radius)
            kws_dist[f"dist{idx_str}"] = Distance(F('ra'), F('dec'), ra, dec)

        return queryset.annotate(**kws_query).filter(filter).annotate(**kws_dist)
    else:
        return queryset.filter(filter)