from django.urls import path, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
# from ifuapp import representations as rep
from ifuapp import models, views
from drf_yasg.generators import OpenAPISchemaGenerator

# Setup OpenAPI generator and cutomize it


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        """Generate a :class:`.Swagger` object with Model description field"""

        swagger = super().get_schema(request, public)

        for name, schema in swagger.definitions.items():
            model = getattr(models, name)
            schema['description'] = model.__doc__
            schema['table_name'] = model._meta.db_table

        return swagger


schema_view = get_schema_view(
    openapi.Info(
        title="IFU Visualiser API",
        default_version='v1',
        description="API of the service for visualization and exploration of spectroscopy IFU data from the MaNGA, SAMI, Califa, and Atlas3D galaxy surveys.",
        contact=openapi.Contact(email="admin@voxastro.org"),
    ),
    generator_class=CustomOpenAPISchemaGenerator,
    public=True,
    permission_classes=[permissions.AllowAny],
)


router = routers.DefaultRouter()
router.register(r'cubes', views.CubeViewSet, basename="cube")
router.register(r'atlas_param', views.AtlasParamViewSet,
                basename="atlas_param")
router.register(r'atlas_morphkin', views.AtlasMorphkinViewSet,
                basename="atlas_morphkin")
router.register(r'califa_object', views.CalifaObjectViewSet,
                basename="califa_object")
router.register(r'sami_cube_obs', views.SamiCubeObsViewSet,
                basename="sami_cube_obs")


urlpatterns = [
    # path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('api/', include(router.urls)),
    # re_path(r'api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'api/swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
