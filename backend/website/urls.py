"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from ifuapp.representations import CubeViewSet, Cube2ViewSet, Cube3ViewSet
# from ifuapp.cube import CubeViewSet


router = routers.DefaultRouter()
router.register(r'cubes', CubeViewSet, basename="cube")
router.register(r'cubes2', Cube2ViewSet)
router.register(r'cubes3', Cube3ViewSet)
# router.register(r'cubes', CubeViewSet)


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('silk/', include('silk.urls', namespace='silk')),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('api/', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns
