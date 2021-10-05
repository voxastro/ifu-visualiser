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

###############################################################################
# GraphQL representation


class AtlasMorphkinType(DjangoObjectType):
    class Meta:
        model = AtlasMorphkin
        description = AtlasMorphkin.__doc__
        filter_fields = ()
        fields = ("__all__")


class Query(graphene.ObjectType):
    atlas_morphkin = graphene.Field(
        AtlasMorphkinType, atlas_name=graphene.String(required=True))
    all_atlas_morphkin = DjangoPaginationConnectionField(AtlasMorphkinType)

    def resolve_all_atlas_morphkin(root, info, **kwargs):
        return AtlasMorphkin.objects.all()

    def resolve_atlas_morphkin(root, info, atlas_name):
        try:
            return AtlasMorphkin.objects.get(atlas_name=atlas_name)
        except AtlasMorphkin.DoesNotExist:
            return None


schema_atlas_morphkin = graphene.Schema(query=Query)
