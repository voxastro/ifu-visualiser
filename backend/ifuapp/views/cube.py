import numpy as np
from django.db import models
from django.shortcuts import get_object_or_404

from rest_framework import serializers, viewsets, response
from rest_flex_fields import FlexFieldsModelSerializer

import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType
from graphene_django_pagination import DjangoPaginationConnectionField

from ifuapp.utils import npl
from ifuapp.pagination import EnhancedPageNumberPagination

from ..utils import apply_search

from ifuapp.models import Cube

from ifuapp.views import (
    AtlasParamSerializer,
    AtlasMorphkinSerializer,
    CalifaObjectSerializer,
    SamiCubeObsSerializer,
    SamiInputcatGamaSerializer,
    SamiInputcatFillerSerializer,
    SamiDensityCatSerializer,
    SamiInputcatClustersSerializer,
    SamiMGEPhotomUnregSerializer,
    SamiGasKinPASerializer,
    MangaDrpSerializer,
)


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

        expandable_fields = {
            'atlas_param': (AtlasParamSerializer, {'many': False}),
            'atlas_morphkin': (AtlasMorphkinSerializer, {'many': False}),
            'califa_object': (CalifaObjectSerializer, {'many': False}),
            'sami_cube_obs': (SamiCubeObsSerializer, {'many': False}),
            'sami_inputcat_gama': (SamiInputcatGamaSerializer, {'many': False}),
            'sami_inputcat_filler': (SamiInputcatFillerSerializer, {'many': False}),
            'sami_densitycat': (SamiDensityCatSerializer, {'many': False}),
            'sami_inputcat_clusters': (SamiInputcatClustersSerializer, {'many': False}),
            'sami_mgephotom_unreg': (SamiMGEPhotomUnregSerializer, {'many': True}),
            'sami_gaskin': (SamiGasKinPASerializer, {'many': True}),
            'manga_drp': (MangaDrpSerializer, {'many': False}),
        }

    def get_spectrum(self, obj):
        request = self.context.get('request')
        ra = request.query_params.get('ra', None)
        dec = request.query_params.get('dec', None)
        arcsec_x = request.query_params.get('arcsec_x', None)
        arcsec_y = request.query_params.get('arcsec_y', None)
        args = [v for v in (ra, dec, arcsec_x, arcsec_y) if v is not None]
        return obj.get_spectrum(*args)

    def get_dist(self, obj):
        try:
            return obj.dist
        except:
            return None


# class CubeViewSet(viewsets.ReadOnlyModelViewSet):
#     __doc__ = Cube.__doc__

#     pagination_class = EnhancedPageNumberPagination
#     serializer_class = CubeSerializer

#     def get_queryset(self):
#         search_query = self.request.query_params.get('q', False)
#         sortby = self.request.query_params.get('sortby', 'cube_id')
#         # in case sort by related field
#         sortby = sortby.replace('.', '__')
#         descending = self.request.query_params.get('descending', 'false')

#         if descending == 'true':
#             sortby = f"-{sortby}"

#         relations = (
#             'atlas_param',
#             'atlas_morphkin',
#             'califa_object',
#             'sami_cube_obs',
#             'sami_inputcat_gama',
#             'manga_drp',
#         )
#         qsall = Cube.objects.all().select_related(*relations)

#         if search_query:
#             return apply_search(qsall, search_query).order_by(sortby)
#         else:
#             return qsall.order_by(sortby)


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

        relations = (
            'atlas_param',
            'atlas_morphkin',
            'califa_object',
            'sami_cube_obs',
            'sami_inputcat_gama',
            'sami_inputcat_filler',
            'sami_densitycat',
            # sami_starcat_clust',
            'sami_inputcat_clusters',
            # 'sami_mgephotom_unreg',
            'manga_drp',
        )
        qsall = Cube.objects.all().select_related(*relations)

        if search_query:
            return apply_search(qsall, search_query).order_by(sortby)
        else:
            return qsall.order_by(sortby)

    def list(self, request):
        queryset = self.get_queryset()
        queryset_paginated = self.paginate_queryset(queryset)
        omit = ['spectrum', 'fov_fits', 'fov_ifu']
        serializer = self.serializer_class(queryset_paginated, many=True,
                                           context={'request': request},
                                           omit=omit)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        cube = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(cube, context={'request': request})
        return response.Response(serializer.data)


###############################################################################
# GraphQL

# class CubeType(DjangoObjectType):
#     class Meta:
#         model = Cube
#         description = Cube.__doc__
#         filter_fields = ()
#         fields = ("__all__")

#     spectrum = GenericScalar(description=Cube.get_spectrum.__doc__)
#     dist = GenericScalar(description="Distance from Cone center")

#     def resolve_spectrum(self, info, **kwargs):
#         return self.get_spectrum()

#     def resolve_dist(self, info, **kwargs):
#         try:
#             return self.dist
#         except:
#             return None


# class Query(graphene.ObjectType):
#     cube = graphene.Field(CubeType, cube_id=graphene.Int(required=True))
#     all_cubes = DjangoPaginationConnectionField(
#         CubeType, query_string=graphene.String())

#     def resolve_all_cubes(root, info, query_string=None, **kwargs):
#         if query_string is not None:
#             return apply_search(Cube.objects.all(), query_string)
#         else:
#             return Cube.objects.all()

#     def resolve_cube(root, info, cube_id):
#         try:
#             return Cube.objects.get(cube_id=cube_id)
#         except Cube.DoesNotExist:
#             return None


# schema_cube = graphene.Schema(query=Query)
