import numpy as np
from django.db import models

from rest_framework import serializers, viewsets, pagination, response
from rest_flex_fields import FlexFieldsModelSerializer
from silk.profiling.profiler import silk_profile
import serpy

from ifuapp.pagination import EnhancedPageNumberPagination
from ifuapp.utils import npl

from ifuapp.models import AtlasMorphkin


###############################################################################
# REST DRF representation (Serializers and ViewSets)


class AtlasMorphkinSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = AtlasMorphkin
        fields = '__all__'


class AtlasMorphkinViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = AtlasMorphkin.__doc__
    queryset = AtlasMorphkin.objects.all()
    pagination_class = EnhancedPageNumberPagination
    serializer_class = AtlasMorphkinSerializer
