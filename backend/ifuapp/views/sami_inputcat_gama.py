import numpy as np
from django.db import models

from rest_framework import serializers, viewsets, pagination, response
from rest_flex_fields import FlexFieldsModelSerializer
from silk.profiling.profiler import silk_profile
import serpy

from ifuapp.pagination import EnhancedPageNumberPagination
from ifuapp.utils import npl

from ifuapp.models import SamiInputcatGama

###############################################################################
# REST DRF representation (Serializers and ViewSets)


class SamiInputcatGamaSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = SamiInputcatGama
        fields = '__all__'


class SamiInputcatGamaViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = SamiInputcatGama.__doc__
    queryset = SamiInputcatGama.objects.all()
    pagination_class = EnhancedPageNumberPagination
    serializer_class = SamiInputcatGamaSerializer
