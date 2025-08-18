from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import LectureViewSet
from .views import NotifyView

router = DefaultRouter()
router.register(r'', LectureViewSet)

urlpatterns = [
    path('notify/', NotifyView, name='notify'), # /api/v1/lectures/notify/...
    path('', include(router.urls)), # /api/v1/lectures/...
]