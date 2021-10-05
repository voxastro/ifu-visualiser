import graphene
from ifuapp.representations import schema_cube, schema_atlas_param, schema_atlas_morphkin


class Query(schema_cube.Query,
            schema_atlas_param.Query,
            schema_atlas_morphkin.Query,):
            # graphene.ObjectType,):
    pass#hello = graphene.String(default_value="Hi there!")


schema = graphene.Schema(query=Query)
