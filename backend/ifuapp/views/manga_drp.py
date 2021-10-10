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

from ifuapp.models import MangaDrp

###############################################################################
# REST DRF representation (Serializers and ViewSets)


class MangaDrpSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = MangaDrp
        fields = '__all__'


class MangaDrpViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = MangaDrp.__doc__
    queryset = MangaDrp.objects.all()
    pagination_class = EnhancedPageNumberPagination
    serializer_class = MangaDrpSerializer
