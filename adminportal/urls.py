from django.urls import path
from .views import dashboardTeams
from .views import dashboardUsers, dashboard, downloadExcel, sendMail, updateScore,teaminfo
# from django.conf.urls import url

app_name = 'adminportal'

urlpatterns = [
    path('mail', sendMail.as_view(), name='mail'),
    # path('teamsEsports', dashboardEsportsTeams, name='deteams'),
    path('updateScore/(<str:sport>)/', updateScore, name='uscore'),
    path('teams', dashboardTeams, name='dteams'),
    path('teamdetails',teaminfo , name='teamdetails'),
    path('users', dashboardUsers, name='dusers'),
    path('excel', downloadExcel, name='teamInfo'),
    # path('excelEsports', downloadEsportsExcel, name='esportsInfo'),
    path('', dashboard, name='dashboard'),
]
