from .views import RegisterView, DisplayProfile, joinTeam, DisplayTeam, leaveTeam, UserViewSet, GroupViewSet, EsportsRegisterViewValorant,send_otp,resend_otp,verify_otp,check_password_match, EsportsRegisterViewBGMI, EsportsRegisterViewChess, EsportsRegisterView, getAthleticEvents, getBadmintonEvents, getBasketBallEvents, getTableTennisEvents, getVolleyBallEvents
from django.urls import path, include
from rest_framework import routers
from .views import LoginUserView,RegisterUserView
from django.urls import re_path 
app_name = 'accounts'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', RegisterView.as_view(), name='register'),
    path('userregister/',RegisterUserView.as_view(),name='userregister'),
    path('userlogin/',LoginUserView,name='userlogin'),
    re_path(r'profile$', DisplayProfile, name='profile'),
    path('EsportsRegister/', EsportsRegisterView, name='EsportsRegister'),
    path(r'EsportsRegister/Valorant/', EsportsRegisterViewValorant.as_view(), name='EsportsRegisterValorant'),
    path(r'EsportsRegister/BGMI/', EsportsRegisterViewBGMI.as_view(), name='EsportsRegisterBGMI'),
    path(r'EsportsRegister/Chess/', EsportsRegisterViewChess.as_view(), name='EsportsRegisterChess'),
    re_path(r'^myTeam$', DisplayTeam, name='myTeam'),
    re_path(r'joinTeam$', joinTeam, name='joinTeam'),
    re_path(r'^leaveTeam$', leaveTeam, name='leaveTeam'),
    path('athletics/', getAthleticEvents, name='athleticEvents'),
    path('badminton/', getBadmintonEvents, name='badmintonEvents'),
    path('tabletennis/', getTableTennisEvents, name='tabletennisEvents'),
    path('voleyball/', getVolleyBallEvents, name='volleyballEvents'),
    path('basketball/', getBasketBallEvents, name='basketballEvents'),
    path('change-password/',check_password_match,name="change_password"),
    path('verify-otp/',verify_otp,name="verify-otp"),
    path('resend-otp/',resend_otp,name="resend-otp"),
    path('send-otp/',send_otp,name="send-otp"),
    
]
