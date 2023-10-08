from django.urls import path, include
from rest_framework import routers
<<<<<<< HEAD
from .views import SponsorView, SponsorViewSet,get_all_sponsors
=======
from .views import SponsorViewSet, SponsorSet
>>>>>>> 4e91eb38d449294a38a8b441e01997f9bc5d6043

app_name = 'sponsor'

router = routers.DefaultRouter()
router.register(r'sponsor', SponsorViewSet, basename='sponsor')
router.register(r'sponsortype', SponsorSet, basename='sponsortype')


urlpatterns = [
<<<<<<< HEAD
    path('', SponsorView.as_view(), name='index'),
    path('sponsorapi/<int:pk>/', include(router.urls)),
    path('getsponsors/', get_all_sponsors, name='get_all_sponsors'),
=======
    path('sponsorapi/', include((router.urls, 'sponsor'), namespace='sponsor-api')),
>>>>>>> 4e91eb38d449294a38a8b441e01997f9bc5d6043
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
