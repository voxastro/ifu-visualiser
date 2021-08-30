import numpy as np
from django.db import models
from rest_framework import serializers, viewsets, pagination, response
from ifuapp.pagination import EnhancedPageNumberPagination
from ifuapp.utils import npl
from silk.profiling.profiler import silk_profile
import serpy
from rest_flex_fields import FlexFieldsModelSerializer

import graphene
from graphene_django import DjangoObjectType, DjangoListField
from graphene.types.generic import GenericScalar
from graphene_django_pagination import DjangoPaginationConnectionField

from ifuapp.models import AtlasParam


###############################################################################
# REST DRF representation (Serializers and ViewSets)


class AtlasParamSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = AtlasParam
        fields = '__all__'


class AtlasParamViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows AtlasParam to be viewed.
    """
    queryset = AtlasParam.objects.all()
    pagination_class = EnhancedPageNumberPagination
    serializer_class = AtlasParamSerializer

###############################################################################
# GraphQL representation


class AtlasParamType(DjangoObjectType):
    class Meta:
        model = AtlasParam
        description = AtlasParam.__doc__
        filter_fields = ()
        fields = ("__all__")


class Query(graphene.ObjectType):
    atlas_param = graphene.Field(
        AtlasParamType, atlas_name=graphene.String(required=True))
    all_atlas_param = DjangoPaginationConnectionField(AtlasParamType)

    def resolve_all_atlas_param(root, info, **kwargs):
        return AtlasParam.objects.all()

    def resolve_atlas_param(root, info, atlas_name):
        try:
            return AtlasParam.objects.get(atlas_name=atlas_name)
        except AtlasParam.DoesNotExist:
            return None


schema_atlas_param = graphene.Schema(query=Query)
