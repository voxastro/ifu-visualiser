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

###############################################################################
# GraphQL representation


class SamiCubeObsType(DjangoObjectType):
    class Meta:
        model = SamiCubeObs
        description = SamiCubeObs.__doc__
        filter_fields = ()
        fields = ("__all__")


class Query(graphene.ObjectType):
    sami_cube_obs = graphene.Field(
        SamiCubeObsType, atlas_name=graphene.String(required=True))
    all_sami_cube_obs = DjangoPaginationConnectionField(SamiCubeObsType)

    def resolve_all_sami_cube_obs(root, info, **kwargs):
        return SamiCubeObs.objects.all()

    def resolve_sami_cube_obs(root, info, atlas_name):
        try:
            return SamiCubeObs.objects.get(atlas_name=atlas_name)
        except SamiCubeObs.DoesNotExist:
            return None


schema_sami_cube_obs = graphene.Schema(query=Query)
