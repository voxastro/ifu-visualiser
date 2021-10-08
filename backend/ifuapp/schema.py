import graphene
from ifuapp.representations import (schema_cube, schema_atlas_param,
                                    schema_atlas_morphkin, schema_califa_object,
                                    schema_sami_cube_obs)


class Query(schema_cube.Query,
            schema_atlas_param.Query,
            schema_atlas_morphkin.Query,
            schema_califa_object.Query,
            schema_sami_cube_obs.Query,):
    # graphene.ObjectType,):
    pass  # hello = graphene.String(default_value="Hi there!")


schema = graphene.Schema(query=Query)
