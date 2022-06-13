import numpy as np
from django.db import models

from rest_framework import serializers, viewsets, pagination, response
from rest_flex_fields import FlexFieldsModelSerializer
from silk.profiling.profiler import silk_profile
import serpy

from ifuapp.pagination import EnhancedPageNumberPagination
from ifuapp.utils import npl


from ifuapp.models import SamiGasKinPA

###############################################################################
# REST DRF representation (Serializers and ViewSets)


class SamiGasKinPASerializer(FlexFieldsModelSerializer):
    class Meta:
        model = SamiGasKinPA
        # fields = '__all__'
        exclude = ('cube',)


class SamiGasKinPAViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = SamiGasKinPA.__doc__
    queryset = SamiGasKinPA.objects.all()
    pagination_class = EnhancedPageNumberPagination
    serializer_class = SamiGasKinPASerializer
