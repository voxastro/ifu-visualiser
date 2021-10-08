import numpy as np
from django.db import models
from rest_framework import serializers, viewsets
from ifuapp.pagination import EnhancedPageNumberPagination
from ifuapp.utils import npl
from rest_flex_fields import FlexFieldsModelSerializer

import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType
from graphene_django_pagination import DjangoPaginationConnectionField
# from djangoql.queryset import apply_search

from ..utils import apply_search
from ifuapp.models import Cube
from .atlas_param import AtlasParamSerializer
from .atlas_morphkin import AtlasMorphkinSerializer
from .califa_object import CalifaObjectSerializer
from .sami_cube_obs import SamiCubeObsSerializer


###############################################################################
# REST DRF representation (Serializers and ViewSets)


class CubeSerializer(FlexFieldsModelSerializer):
    spectrum = serializers.SerializerMethodField()
    dist = serializers.SerializerMethodField()

    class Meta:
        model = Cube
        # hide related fields to avoid field duplication
        fields = [
            f.name for f in Cube._meta.fields if f.related_model is None] + ['spectrum', 'dist']
        # omit = ['spectrum', 'dist']

        expandable_fields = {
            'atlas_param': (AtlasParamSerializer, {'many': False}),
            'atlas_morphkin': (AtlasMorphkinSerializer, {'many': False}),
            'califa_object': (CalifaObjectSerializer, {'many': False}),
            'sami_cube_obs': (SamiCubeObsSerializer, {'many': False}),
        }

    def get_spectrum(self, obj):
        return obj.get_spectrum()

    def get_dist(self, obj):
        try:
            return obj.dist
        except:
            return None


class CubeViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = Cube.__doc__

    pagination_class = EnhancedPageNumberPagination
    serializer_class = CubeSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('q', False)
        sortby = self.request.query_params.get('sortby', 'cube_id')
        # in case sort by related field
        sortby = sortby.replace('.', '__')
        descending = self.request.query_params.get('descending', 'false')

        if descending == 'true':
            sortby = f"-{sortby}"

        qsall = Cube.objects.all().select_related(
            'atlas_param', 'atlas_morphkin', 'califa_object')

        if search_query:
            return apply_search(qsall, search_query).order_by(sortby)
        else:
            return qsall.order_by(sortby)


###############################################################################
# GraphQL

class CubeType(DjangoObjectType):
    class Meta:
        model = Cube
        description = Cube.__doc__
        filter_fields = ()
        fields = ("__all__")

    spectrum = GenericScalar(description=Cube.get_spectrum.__doc__)
    dist = GenericScalar(description="Distance from Cone center")

    def resolve_spectrum(self, info, **kwargs):
        return self.get_spectrum()

    def resolve_dist(self, info, **kwargs):
        try:
            return self.dist
        except:
            return None


class Query(graphene.ObjectType):
    cube = graphene.Field(CubeType, cube_id=graphene.Int(required=True))
    all_cubes = DjangoPaginationConnectionField(
        CubeType, query_string=graphene.String())

    def resolve_all_cubes(root, info, query_string=None, **kwargs):
        if query_string is not None:
            return apply_search(Cube.objects.all(), query_string)
        else:
            return Cube.objects.all()

    def resolve_cube(root, info, cube_id):
        try:
            return Cube.objects.get(cube_id=cube_id)
        except Cube.DoesNotExist:
            return None


schema_cube = graphene.Schema(query=Query)
