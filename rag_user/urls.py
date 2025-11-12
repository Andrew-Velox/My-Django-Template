from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()
# router.register(r'list', UserViewSet, basename='users')      # will be /user/list/
router.register(r'register', RegistrationViewSet, basename='register')  # will be /user/register/


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegistrationViewSet.as_view({'post': 'create'}), name='user-register'),
    path('account/active/<uid64>/<token>/', activate, name='activate'),
]