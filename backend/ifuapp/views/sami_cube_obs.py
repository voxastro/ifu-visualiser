import numpy as np
from django.db import models

from rest_framework import serializers, viewsets, pagination, response
from rest_flex_fields import FlexFieldsModelSerializer
from silk.profiling.profiler import silk_profile
import serpy

from ifuapp.pagination import EnhancedPageNumberPagination
from ifuapp.utils import npl

from ifuapp.models import SamiCubeObs

###############################################################################
# REST DRF representation (Serializers and ViewSets)


class SamiCubeObsSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = SamiCubeObs
        fields = '__all__'


class SamiCubeObsViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = SamiCubeObs.__doc__
    queryset = SamiCubeObs.objects.all()
    pagination_class = EnhancedPageNumberPagination
    serializer_class = SamiCubeObsSerializer

