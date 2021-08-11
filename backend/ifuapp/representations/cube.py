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
import graphene_django_optimizer as gql_optimizer

from ifuapp.models import Cube
from ifuapp.utils import apply_search
from .atlas_param import AtlasParamSerializer
from .atlas_morphkin import AtlasMorphkinSerializer

###############################################################################
# REST DRF representation (Serializers and ViewSets)


class CubeSerializer(FlexFieldsModelSerializer):
    spectrum = serializers.SerializerMethodField()

    class Meta:
        model = Cube
        fields = '__all__'

        expandable_fields = {
            'atlas_param': (AtlasParamSerializer, {'many': True}),
            'atlas_morphkin': (AtlasMorphkinSerializer, {'many': True})
        }

    def get_spectrum(self, obj):
        return obj.get_spectrum()


class CubeSerializerSerpy(serpy.Serializer):
    cube_id = serpy.IntField()
    ra = serpy.FloatField()
    dec = serpy.FloatField()
    survey = serpy.StrField()
    filename = serpy.StrField()
    exptime = serpy.FloatField(required=False)
    manga_id = serpy.StrField()
    manga_plateifu = serpy.StrField()
    sami_catid = serpy.StrField()
    sami_cube = serpy.StrField()
    califa_id = serpy.StrField()
    califa_name = serpy.StrField()
    califa_cube = serpy.StrField()
    atlas_name = serpy.StrField()
    spectrum = serpy.MethodField()

    def get_spectrum(self, obj):
        return obj.get_spectrum()


class CubeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Cubes to be viewed.
    """
    # @silk_profile(name='ViewSet Cube Get')

    pagination_class = EnhancedPageNumberPagination
    serializer_class = CubeSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('q', False)
        # sortby = self.request.query_params.get('sortby', 'r2id_spec')
        # descending = self.request.query_params.get('descending', 'false')

        # if descending == 'true':
        #     sortby = f"-{sortby}"
        if search_query:
            return apply_search(Cube.objects.all(), search_query)
        else:
            return Cube.objects.all()
        # if search_query:
        #     # Cone Search Query. RA DEC size must be in degrees
        #     if 'cone(' in search_query:
        #         pstr = search_query.replace("%20", "").split(
        #             "cone(")[1].split(")")[0].split(",")
        #         ra, dec, size = [float(p) for p in pstr]
        #         return Spec.objects.extra(
        #             where=[f"crd2000 @ scircle '<({ra}d, {dec}d), {size}d>'"],
        #             select={
        #                 'dist': f"(crd2000 <-> spoint({ra}*pi()/180, {dec}*pi()/180))/pi()*180"}
        #         ).order_by(sortby)
        #     # Custom Parameter Query
        #     else:
        #         from customquery import Parser
        #         parser = Parser(Spec)
        #         flt = parser.parse(search_query)
        #         return Spec.objects.filter(flt).order_by(sortby)
        # else:
        #     return Spec.objects.order_by(sortby)


class Cube2ViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Cubes to be viewed.
    """
    # @silk_profile(name='ViewSet Cube Get')
    queryset = Cube.objects.all()
    pagination_class = EnhancedPageNumberPagination
    serializer_class = CubeSerializerSerpy


class Cube3ViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Cubes to be viewed.
    """
    queryset = Cube.objects.all()
    pagination_class = EnhancedPageNumberPagination
    # pagination_class = pagination.PageNumberPagination
    # serializer_class = CubeSerializerSerpy

    # def list(self, request):
    # return response.Response(self.queryset.values())

    def list(self, request):
        page = self.paginate_queryset(self.queryset.values())
        # data = [dict(
        #     cube_id=q.cube_id,
        #     ra=q.ra,
        #     dec=q.dec,
        #     survey=q.survey,
        #     filename=q.filename,
        #     exptime=q.exptime,
        #     manga_id=q.manga_id,
        #     manga_plateifu=q.manga_plateifu,
        #     sami_catid=q.sami_catid,
        #     sami_cube=q.sami_cube,
        #     califa_id=q.califa_id,
        #     califa_name=q.califa_name,
        #     califa_cube=q.califa_cube,
        #     atlas_name=q.atlas_name,
        # ) for q in self.queryset]

        # return self.get_paginated_response(data)

        return self.get_paginated_response(page)


###############################################################################
# GraphQL

class CubeType(DjangoObjectType):
    class Meta:
        model = Cube
        description = Cube.__doc__
        filter_fields = ()
        fields = ("__all__")

    # spectrum = GenericScalar(description=Cube.get_spectrum.__doc__)

    # def resolve_spectrum(self, info, **kwargs):
    #     return self.get_spectrum()


class Query(graphene.ObjectType):
    cube = graphene.Field(CubeType, cube_id=graphene.Int(required=True))
    all_cubes = DjangoPaginationConnectionField(
        CubeType, query_string=graphene.String())

    def resolve_all_cubes(root, info, query_string=None, **kwargs):
        if query_string is not None:
            return apply_search(Cube.objects.all(), search_query=query_string)
        else:
            return Cube.objects.all()

    def resolve_cube(root, info, cube_id):
        try:
            return Cube.objects.get(cube_id=cube_id)
        except Cube.DoesNotExist:
            return None


schema_cube = graphene.Schema(query=Query)
