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

from ifuapp.models import SamiDensityCat

###############################################################################
# REST DRF representation (Serializers and ViewSets)


class SamiDensityCatSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = SamiDensityCat
        fields = '__all__'


class SamiDensityCatViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = SamiDensityCat.__doc__
    queryset = SamiDensityCat.objects.all()
    pagination_class = EnhancedPageNumberPagination
    serializer_class = SamiDensityCatSerializer
