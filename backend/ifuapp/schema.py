import graphene
from graphene_django import DjangoObjectType, DjangoListField
from ifuapp.models import Cube, AtlasParam


class CubeType(DjangoObjectType):
    class Meta:
        model = Cube
        fields = ("__all__")


class AtlasParamType(DjangoObjectType):
    class Meta:
        model = AtlasParam
        description = AtlasParam.__doc__
        fields = ("__all__")


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")
    all_cubes = graphene.List(CubeType)
    cube = graphene.Field(CubeType, cube_id=graphene.Int(required=True))

    atlas_param = graphene.Field(
        AtlasParamType, cube_id=graphene.Int(required=True), description="Atlas3D main parameters")
    all_atlas_param = graphene.List(AtlasParamType)

    def resolve_all_cubes(root, info):
        return Cube.objects.prefetch_related('atlas_param').all()

    def resolve_cube(root, info, cube_id):
        try:
            return Cube.objects.get(cube_id=cube_id)
        except Cube.DoesNotExist:
            return None

    def resolve_atlas_Param(root, info, cube_id):
        try:
            return AtlasParam.objects.get(cube=cube_id)
        except Cube.DoesNotExist:
            return None

    def resolve_all_atlas_param(root, info):
        return AtlasParam.objects.select_related('cube').all()


schema = graphene.Schema(query=Query)
