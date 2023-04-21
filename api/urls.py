from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from api.views import PostViewSet

router = routers.DefaultRouter()
router.register('posts', PostViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', obtain_auth_token, name="obtain_auth_token"),
]
