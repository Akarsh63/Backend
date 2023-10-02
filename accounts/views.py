from random import random
import uuid
from django.views.generic import CreateView
from .models import UserProfile, EsportsUserProfile,PasswordResetRequest
from .forms import EsportsRegisterFormBGMI, EsportsRegisterFormChess, EsportsRegisterFormValorant, RegisterForm
from django.contrib.auth.views import LoginView
from django.shortcuts import reverse, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from registration.models import TeamRegistration, EsportsTeamRegistration
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer,UserProfileSerializer
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .helpers import generate_otp, send_otp_email, create_reset_request

# api method to register the user 

class RegisterUserView(APIView):
    def post(self, request):
        user1 = User.objects.filter(email=request.data.get('email')).first()
        if user1:
            return Response({"Error": "Email already exists!"}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('password') != request.data.get('confirm_password'):
            return Response({"Error": "Passwords don't match!"}, status=status.HTTP_400_BAD_REQUEST)

        user_data = {
            "username": request.data["email"],
            "email": request.data["email"],
            "first_name": request.data.get("first_name", ""),
            "last_name": request.data.get("last_name", ""),
            "password": request.data["password"],
        }
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            profile_data = {
                "user": user.id,
                "phone": request.data["phone"],
                "gender": request.data["gender"],
                "college": request.data["college"],
                "state": request.data["state"],
                "accommodation_required": request.data["accommodation_required"],
            }

            profile_serializer = UserProfileSerializer(data=profile_data)
            if profile_serializer.is_valid():
                profile_serializer.save()
                return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
            else:
                user.delete() 
                return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user_profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(user_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# api method to login the user 

@api_view(['POST'])
def LoginUserView(request):
      email = request.data['email']
      password = request.data['password']
      user = User.objects.filter(email=email).first()
      if user is None:
            return Response({"message":'User not found!'},status=status.HTTP_404_NOT_FOUND)
      if not user.check_password(password):
            return Response({"message":'Invalid Password or Email'},status=status.HTTP_400_BAD_REQUEST)
      return Response({"message":'User Loged in Successfully!'}, status=status.HTTP_200_OK)
@api_view(['POST'])
def send_otp(request):
    try:
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()  # Get the user with the provided email
        
        if user:
            otp = generate_otp()
            create_reset_request(email, otp)
            send_otp_email(email, otp)
            return JsonResponse({'success': True, 'message': 'OTP sent to your email.'})
        else:
            return JsonResponse({'success': False, 'message': 'Email not found in the database.'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
@api_view(['POST'])
def verify_otp(request):
    try:
        email = request.data['email']
        otp = request.data['otp']

        if PasswordResetRequest.objects.filter(email=email, otp=otp).exists():
            return JsonResponse({'success': True, 'message': 'OTP verified successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid OTP.'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
@api_view(['POST'])
def resend_otp(request):
    try:
        email = request.data['email']

        if User.objects.filter(email=email).exists():
            otp = generate_otp()
            create_reset_request(email, otp)
            send_otp_email(email, otp)
            return JsonResponse({'success': True, 'message': 'OTP resent to your email.'})
        else:
            return JsonResponse({'success': False, 'message': 'Email not found in the database.'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
@api_view(['POST'])
def check_password_match(request):
    try:
        new_password = request.data['new_password']
        confirm_password = request.data['confirm_password']

        if new_password == confirm_password:
            return JsonResponse({'success': True, 'message': 'Passwords match.'})
        else:
            return JsonResponse({'success': False, 'message': 'Passwords do not match.'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'

    def form_valid(self, form):
        data = self.request.POST.copy()
        data['username'] = data['email']
        form = RegisterForm(data)
        user = form.save()
        RegisterView.create_profile(user, **form.cleaned_data)
        return super(RegisterView, self).form_valid(form)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    @staticmethod
    def create_profile(user=None, **kwargs):
        userprofile = UserProfile.objects.create(user=user, gender=kwargs['gender'], phone=kwargs['phone'],
                                                 college=kwargs['college'],
                                                 state=kwargs['state'],
                                                 accommodation_required=kwargs['accommodation_required']
                                                 )
        userprofile.save()


def EsportsRegisterView(request):
    return render(request, 'accounts/EsportsregCards.html')


class EsportsRegisterViewValorant(CreateView):
    form_class = EsportsRegisterFormValorant
    template_name = 'accounts/Esportsregister.html'
    success_url = '/login/'

    def form_valid(self, form):
        data = self.request.POST.copy()
        data['username'] = data['email']
        form = EsportsRegisterFormValorant(data)
        user = form.save()
        EsportsRegisterViewValorant.create_profile(user, **form.cleaned_data)
        return super(EsportsRegisterViewValorant, self).form_valid(form)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    @staticmethod
    def create_profile(user=None, **kwargs):
        userprofile = EsportsUserProfile.objects.create(user=user, gender=kwargs['gender'], phone=kwargs['phone'],
                                                        college=kwargs['college'],
                                                        state=kwargs['state'], captain_ingame_id=kwargs['captain_ingame_id'], captain_rank=kwargs['captain_peak_rank'], team_member2=kwargs['Member_2_Name'], team_member3=kwargs['Member_3_Name'], team_member4=kwargs['Member_4_Name'], team_member5=kwargs['Member_5_Name'], team_member6=kwargs['Member_6_Name'], team_member2_ingame_id=kwargs['Member_2_ingame_id'], team_member3_ingame_id=kwargs[
                                                            'Member_3_ingame_id'], team_member4_ingame_id=kwargs['Member_4_ingame_id'], team_member5_ingame_id=kwargs['Member_5_ingame_id'], team_member6_ingame_id=kwargs['Member_6_ingame_id'], team_member2_rank=kwargs['Member_2_peak_rank'], team_member3_rank=kwargs['Member_3_peak_rank'], team_member4_rank=kwargs['Member_4_peak_rank'], team_member5_rank=kwargs['Member_5_peak_rank'], team_member6_rank=kwargs['Member_6_peak_rank']
                                                        )
        userprofile.save()
        team = EsportsTeamRegistration.objects.create(sport='1', college=kwargs['college'], captian=userprofile)
        spor = EsportsTeamRegistration.ESPORT_CHOICES[int(team.sport)-1][1][:3]
        team.teamId = "VA-" + spor[:3].upper() + '-' + userprofile.user.username[:3].upper() + "{}".format(int(random()*100))
        team.save()
        userprofile.teamId = team
        userprofile.save()


class EsportsRegisterViewBGMI(CreateView):
    form_class = EsportsRegisterFormBGMI
    template_name = 'accounts/Esportsregister.html'
    success_url = '/login/'

    def form_valid(self, form):
        data = self.request.POST.copy()
        data['username'] = data['email']
        form = EsportsRegisterFormBGMI(data)
        user = form.save()
        EsportsRegisterViewBGMI.create_profile(user, **form.cleaned_data)
        return super(EsportsRegisterViewBGMI, self).form_valid(form)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    @staticmethod
    def create_profile(user=None, **kwargs):
        userprofile = EsportsUserProfile.objects.create(user=user, gender=kwargs['gender'], phone=kwargs['phone'],
                                                        college=kwargs['college'],
                                                        state=kwargs['state'], captain_ingame_id=kwargs['captain_character_id'], team_member2=kwargs['Member_2_Name'], team_member3=kwargs['Member_3_Name'], team_member4=kwargs['Member_4_Name'], team_member2_ingame_id=kwargs['Member_2_character_id'], team_member3_ingame_id=kwargs[
                                                            'Member_3_character_id'], team_member4_ingame_id=kwargs['Member_4_character_id'], team_member2_name=kwargs['Member_2_ingame_name'], team_member3_name=kwargs['Member_3_ingame_name'], team_member4_name=kwargs['Member_4_ingame_name']
                                                        )
        userprofile.save()
        team = EsportsTeamRegistration.objects.create(sport='2', college=kwargs['college'], captian=userprofile)
        spor = EsportsTeamRegistration.ESPORT_CHOICES[int(team.sport)-1][1][:3]
        team.teamId = "VA-" + spor[:3].upper() + '-' + userprofile.user.username[:3].upper() + "{}".format(int(random()*100))
        team.save()
        userprofile.teamId = team
        userprofile.save()


class EsportsRegisterViewChess(CreateView):
    form_class = EsportsRegisterFormChess
    template_name = 'accounts/Esportsregister.html'
    success_url = '/login/'

    def form_valid(self, form):
        data = self.request.POST.copy()
        data['username'] = data['email']
        form = EsportsRegisterFormChess(data)
        user = form.save()
        EsportsRegisterViewChess.create_profile(user, **form.cleaned_data)
        return super(EsportsRegisterViewChess, self).form_valid(form)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    @staticmethod
    def create_profile(user=None, **kwargs):
        userprofile = EsportsUserProfile.objects.create(user=user, gender=kwargs['gender'], phone=kwargs['phone'],
                                                        college=kwargs['college'],
                                                        state=kwargs['state'], captain_ingame_id=kwargs['Lichess_id'], team_member2_ingame_id=[
                                                            'Chesscom_id']
                                                        )
        userprofile.save()
        team = EsportsTeamRegistration.objects.create(sport='3', college=kwargs['college'], captian=userprofile)
        spor = EsportsTeamRegistration.ESPORT_CHOICES[int(team.sport)-1][1][:3]
        team.teamId = "VA-" + spor[:3].upper() + '-' + userprofile.user.username[:3].upper() + "{}".format(int(random()*100))
        team.save()
        userprofile.teamId = team
        userprofile.save()


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_redirect_url(self):
        if self.request.user.is_superuser:
            return reverse('adminportal:dashboard')
        else:
            return reverse('main:home')


@login_required(login_url="login")
def DisplayProfile(request):
    try:
        user = get_object_or_404(UserProfile, user=request.user)
    except:
        user = get_object_or_404(EsportsUserProfile, user=request.user)
    return render(request, 'accounts/profile.html', {'userprofile': user, 'user': request.user, 'page': "profile"})


@login_required(login_url="login")
def DisplayTeam(request):
    try:
        user = get_object_or_404(UserProfile, user=request.user)
    except:
        user = get_object_or_404(EsportsUserProfile, user=request.user)
    teamId = user.teamId
    try:
        team = get_object_or_404(TeamRegistration, teamId=teamId)
    except:
        team = get_object_or_404(EsportsTeamRegistration, teamId=teamId)

    if team.subevents is not None:
        subevents = team.subevents.split(', ')
        return render(request, 'accounts/myTeam.html', {'profile_team': team, 'profile_user': user, 'page': "team", 'user': request.user, 'userprofile': user, 'subevents': subevents})

    return render(request, 'accounts/myTeam.html', {'profile_team': team, 'profile_user': user, 'page': "team", 'user': request.user, 'userprofile': user})


@login_required(login_url="login")
def getAthleticEvents(request):
    registeredEvents = []

    A100m = request.POST.get('100m', 'false')
    if A100m != 'false':
        registeredEvents.append('100m')
    A200m = request.POST.get('200m', 'false')
    if A200m != 'false':
        registeredEvents.append('200m')
    A400m = request.POST.get('400m', 'false')
    if A400m != 'false':
        registeredEvents.append('400m')
    A800m = request.POST.get('800m', 'false')
    if A800m != 'false':
        registeredEvents.append('800m')
    A1500m = request.POST.get('1500m', 'false')
    if A1500m != 'false':
        registeredEvents.append('1500m')
    A5000m = request.POST.get('5000m', 'false')
    if A5000m != 'false':
        registeredEvents.append('5000m')
    A4x100m = request.POST.get('4*100m', 'false')
    if A4x100m != 'false':
        registeredEvents.append('4*100m')
    A4x400m = request.POST.get('4*400m', 'false')
    if A4x400m != 'false':
        registeredEvents.append('4*400m')

    registeredEvents = ', '.join(registeredEvents)

    try:
        user = get_object_or_404(UserProfile, user=request.user)
    except:
        user = get_object_or_404(EsportsUserProfile, user=request.user)
    teamId = user.teamId
    try:
        team = get_object_or_404(TeamRegistration, teamId=teamId)
    except:
        team = get_object_or_404(EsportsTeamRegistration, teamId=teamId)

    team.subevents = registeredEvents
    team.save()

    return redirect('accounts:myTeam')


@login_required(login_url="login")
def getBadmintonEvents(request):
    registeredEvents = []

    Male = request.POST.get('Male', 'false')
    if Male != 'false':
        registeredEvents.append('Male')
    Female = request.POST.get('Female', 'false')
    if Female != 'false':
        registeredEvents.append('Female')
    Mixed = request.POST.get('mixed', 'false')
    if Mixed != 'false':
        registeredEvents.append('mixed')

    registeredEvents = ', '.join(registeredEvents)

    try:
        user = get_object_or_404(UserProfile, user=request.user)
    except:
        user = get_object_or_404(EsportsUserProfile, user=request.user)
    teamId = user.teamId
    try:
        team = get_object_or_404(TeamRegistration, teamId=teamId)
    except:
        team = get_object_or_404(EsportsTeamRegistration, teamId=teamId)

    team.subevents = registeredEvents
    team.save()

    return redirect('accounts:myTeam')


@login_required(login_url="login")
def getTableTennisEvents(request):
    registeredEvents = []

    Male = request.POST.get('Male', 'false')
    if Male != 'false':
        registeredEvents.append('Male')
    Female = request.POST.get('Female', 'false')
    if Female != 'false':
        registeredEvents.append('Female')
    Mixed = request.POST.get('mixed', 'false')
    if Mixed != 'false':
        registeredEvents.append('mixed')

    registeredEvents = ', '.join(registeredEvents)

    try:
        user = get_object_or_404(UserProfile, user=request.user)
    except:
        user = get_object_or_404(EsportsUserProfile, user=request.user)
    teamId = user.teamId
    try:
        team = get_object_or_404(TeamRegistration, teamId=teamId)
    except:
        team = get_object_or_404(EsportsTeamRegistration, teamId=teamId)

    team.subevents = registeredEvents
    team.save()

    return redirect('accounts:myTeam')


@login_required(login_url="login")
def getBasketBallEvents(request):
    registeredEvents = []

    Male = request.POST.get('Male', 'false')
    if Male != 'false':
        registeredEvents.append('Male')
    Female = request.POST.get('Female', 'false')
    if Female != 'false':
        registeredEvents.append('Female')

    registeredEvents = ', '.join(registeredEvents)

    try:
        user = get_object_or_404(UserProfile, user=request.user)
    except:
        user = get_object_or_404(EsportsUserProfile, user=request.user)
    teamId = user.teamId
    try:
        team = get_object_or_404(TeamRegistration, teamId=teamId)
    except:
        team = get_object_or_404(EsportsTeamRegistration, teamId=teamId)

    team.subevents = registeredEvents
    team.save()

    return redirect('accounts:myTeam')


@login_required(login_url="login")
def getVolleyBallEvents(request):
    registeredEvents = []

    Male = request.POST.get('Male', 'false')
    if Male != 'false':
        registeredEvents.append('Male')
    Female = request.POST.get('Female', 'false')
    if Female != 'false':
        registeredEvents.append('Female')

    registeredEvents = ', '.join(registeredEvents)

    try:
        user = get_object_or_404(UserProfile, user=request.user)
    except:
        user = get_object_or_404(EsportsUserProfile, user=request.user)
    teamId = user.teamId
    try:
        team = get_object_or_404(TeamRegistration, teamId=teamId)
    except:
        team = get_object_or_404(EsportsTeamRegistration, teamId=teamId)

    team.subevents = registeredEvents
    team.save()

    return redirect('accounts:myTeam')


@login_required(login_url="login")
def leaveTeam(request):
    user = get_object_or_404(UserProfile, user=request.user)
    teamId = user.teamId
    team = get_object_or_404(TeamRegistration, teamId=teamId)
    if user == team.captian:
        team.delete()
    else:
        user.teamId = None
        user.save()
    return redirect('main:home')


@login_required(login_url="login")
def joinTeam(request):
    user = request.user
    if request.method == 'POST':
        teamId = request.POST.get('teamId')
        if user is not None:
            user = get_object_or_404(UserProfile, user=user)
            if user.teamId is not None:
                message = "You are already in team {}".format(user.teamId)
                message += "\nYou have to register again to join another team. \nContact Varchas administrators."
                return HttpResponse(message, content_type="text/plain")
            team = get_object_or_404(TeamRegistration, teamId=teamId)
            user.teamId = team
            user.save()
            return redirect('accounts:myTeam')
        return reverse('login')
    return render(request, 'accounts/joinTeam.html')


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]
