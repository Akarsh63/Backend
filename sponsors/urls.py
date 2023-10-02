from django.urls import path, include
from rest_framework import routers
from .views import SponsorView, SponsorViewSet,get_all_sponsors

app_name = 'sponsor'

router = routers.DefaultRouter()
router.register(r'sponsor', SponsorViewSet)

urlpatterns = [
    path('', SponsorView.as_view(), name='index'),
    path('sponsorapi/<int:pk>/', include(router.urls)),
    path('getsponsors/', get_all_sponsors, name='get_all_sponsors'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
