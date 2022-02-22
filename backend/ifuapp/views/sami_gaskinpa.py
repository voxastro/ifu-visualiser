import numpy as np
from django.db import models

from rest_framework import serializers, viewsets, pagination, response
from rest_flex_fields import FlexFieldsModelSerializer
from silk.profiling.profiler import silk_profile
import serpy

from ifuapp.pagination import EnhancedPageNumberPagination
from ifuapp.utils import npl

import graphene
from graphene_django import DjangoObjectType, DjangoListField
from graphene.types.generic import GenericScalar
from graphene_django_pagination import DjangoPaginationConnectionField

from ifuapp.models import SamiGasKinPA

###############################################################################
# REST DRF representation (Serializers and ViewSets)

class SamiGaskinPASerializer(FlexFieldsModelSerializer):
    class Meta:
        model = SamiGasKinPA
        fields = '__all__'


class SamiGaskinPAViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = SamiGasKinPA.__doc__
    queryset = SamiGasKinPA.objects.all()
    pagination_class = EnhancedPageNumberPagination
    serializer_class = SamiGaskinPASerializer
