import numpy as np
from django.db import models

from rest_framework import serializers, viewsets, pagination, response
from rest_flex_fields import FlexFieldsModelSerializer
from silk.profiling.profiler import silk_profile
import serpy

from ifuapp.pagination import EnhancedPageNumberPagination
from ifuapp.utils import npl


from ifuapp.models import CalifaObject


###############################################################################
# REST DRF representation (Serializers and ViewSets)


class CalifaObjectSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = CalifaObject
        fields = '__all__'


class CalifaObjectViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = CalifaObject.__doc__
    queryset = CalifaObject.objects.all()
    pagination_class = EnhancedPageNumberPagination
    serializer_class = CalifaObjectSerializer

