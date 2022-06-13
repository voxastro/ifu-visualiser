import numpy as np
from django.db import models

from rest_framework import serializers, viewsets, pagination, response
from rest_flex_fields import FlexFieldsModelSerializer
from silk.profiling.profiler import silk_profile
import serpy

from ifuapp.pagination import EnhancedPageNumberPagination
from ifuapp.utils import npl


from ifuapp.models import SamiInputcatClusters

###############################################################################
# REST DRF representation (Serializers and ViewSets)


class SamiInputcatClustersSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = SamiInputcatClusters
        fields = '__all__'


class SamiInputcatClustersViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = SamiInputcatClusters.__doc__
    queryset = SamiInputcatClusters.objects.all()
    pagination_class = EnhancedPageNumberPagination
    serializer_class = SamiInputcatClustersSerializer
