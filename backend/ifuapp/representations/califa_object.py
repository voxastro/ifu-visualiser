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

###############################################################################
# GraphQL representation


class CalifaObjectType(DjangoObjectType):
    class Meta:
        model = CalifaObject
        description = CalifaObject.__doc__
        filter_fields = ()
        fields = ("__all__")


class Query(graphene.ObjectType):
    califa_object = graphene.Field(
        CalifaObjectType, atlas_name=graphene.String(required=True))
    all_califa_object = DjangoPaginationConnectionField(CalifaObjectType)

    def resolve_all_califa_object(root, info, **kwargs):
        return CalifaObject.objects.all()

    def resolve_califa_object(root, info, atlas_name):
        try:
            return CalifaObject.objects.get(atlas_name=atlas_name)
        except CalifaObject.DoesNotExist:
            return None


schema_califa_object = graphene.Schema(query=Query)
