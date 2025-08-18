from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import LINEAPIView, UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('', include(router.urls)), # api/v1/users/...
    path('line/', LINEAPIView.as_view(), name='line-webhook'), # api/v1/users/line/...
]