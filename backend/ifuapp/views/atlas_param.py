import numpy as np
from django.db import models

from rest_framework import serializers, viewsets, pagination, response
from rest_flex_fields import FlexFieldsModelSerializer
from silk.profiling.profiler import silk_profile
import serpy

from ifuapp.pagination import EnhancedPageNumberPagination
from ifuapp.utils import npl
from ifuapp.models import AtlasParam


###############################################################################
# REST DRF representation (Serializers and ViewSets)


class AtlasParamSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = AtlasParam
        fields = '__all__'


class AtlasParamViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = AtlasParam.__doc__
    queryset = AtlasParam.objects.all()
    pagination_class = EnhancedPageNumberPagination
    serializer_class = AtlasParamSerializer

