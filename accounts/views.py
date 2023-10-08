<<<<<<< HEAD
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
=======
import random
from .models import UserProfile,PasswordResetRequest
from django.utils import timezone
from django.shortcuts import get_object_or_404
from registration.models import TeamRegistration
>>>>>>> 4e91eb38d449294a38a8b441e01997f9bc5d6043
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer,UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
<<<<<<< HEAD
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .helpers import generate_otp, send_otp_email, create_reset_request
=======
from rest_framework.decorators import api_view,permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.views import LoginView
from django.shortcuts import reverse, redirect
from django.contrib.auth.hashers import make_password
>>>>>>> 4e91eb38d449294a38a8b441e01997f9bc5d6043

# api method to register the user 

class RegisterUserView(APIView):
    def post(self, request):
        user1 = User.objects.filter(email=request.data.get('email')).first()
        if user1:
            return Response({"Error": "Email already exists!"}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('password') != request.data.get('confirm_password'):
            return Response({"Error": "Passwords don't match!"}, status=status.HTTP_400_BAD_REQUEST)
        hashed_password = make_password(request.data["password"])
        user_data = {
            "username": request.data["email"],
            "email": request.data["email"],
            "first_name": request.data.get("first_name", ""),
            "last_name": request.data.get("last_name", ""),
            "password": hashed_password,
        }
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            if len(request.data['phone']) > 10:
                return Response({"Error": "Phone number must be 10 digits"}, status=status.HTTP_400_BAD_REQUEST)
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
                return Response({"message":'User created Successfully'}, status=status.HTTP_201_CREATED)
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
<<<<<<< HEAD
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


=======
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = User.objects.filter(email=email).first()
    
    if user is None:
        return Response({"message": 'User not found!'}, status=status.HTTP_404_NOT_FOUND)
    
    if not user.check_password(password):
        return Response({"message": 'Invalid Password or Email'}, status=status.HTTP_400_BAD_REQUEST)

    # Generate a JWT token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)  # Extract the refresh token value

    return Response({"message": 'User Logged in Successfully!', "access_token": access_token, "refresh_token": refresh_token}, status=status.HTTP_200_OK)

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_redirect_url(self):
        if self.request.user.is_superuser:
            return reverse('adminportal:dashboard')
        else:
            return reverse('main:home')

class PasswordReset(APIView):
    def post(self,request):
         email = request.data.get('email')
         user=get_object_or_404(User,email=email)
         if not user:
             return Response({"message":"Sorry! User not found"},status=status.HTTP_404_NOT_FOUND)
         otp = random.randint(1000, 9999)
         try :
             reset_request=PasswordResetRequest.objects.get(email=email)
             reset_request.otp=otp
             reset_request.save()
         except:
            reset_request = PasswordResetRequest(user=user,email=email,otp=otp)
            reset_request.save()
         subject='Varchas23 | OTP Verification'
         message = f'Hi {user.username}, Here is your otp {otp}.'
         email_from = settings.EMAIL_HOST_USER
         recipient_list = [user.email, ]
         send_mail( subject, message, email_from, recipient_list )
         return Response({"message":"OTP sent Successfully!"},status=status.HTTP_201_CREATED)         

class OTPVerification(APIView):
    def post(self, request):
        email_req = request.data['email']
        otp = request.data.get('otp')

        try:
            reset_request =PasswordResetRequest.objects.filter(email=email_req).first()
        except PasswordResetRequest.DoesNotExist:
            return Response({"message": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)
        if reset_request.expiration_time < timezone.now():
            return Response({"message": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

        if reset_request.otp != int(otp):
            return Response({"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def resendpassword(request):
    email_req=request.data.get('email')
    user=get_object_or_404(User,email=email_req)
    if not user:
        return Response({"message":"Sorry! User not found"},status=status.HTTP_404_NOT_FOUND)
    try:
        reset_request=PasswordResetRequest.objects.get(email=email_req)
    except:
        return Response({"message": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)     
    otp = random.randint(1000, 9999)
    reset_request.otp=otp
    reset_request.save()
    subject='Varchas23 | OTP Verification'
    message = f'Hi {user.username}, Here is your otp {otp}.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    send_mail( subject, message, email_from, recipient_list )
    return Response({"message":"OTP sent Successfully!"},status=status.HTTP_201_CREATED) 

@api_view(['POST'])
def restpassword(request):
    email_req=request.data.get('email')
    password=request.data.get('password')
    try:
        user=User.objects.get(email=email_req)
    except:
        return Response({"message":"Sorry! User not found"},status=status.HTTP_404_NOT_FOUND)
    user.set_password(password)
    user.save()
    return Response({"message":"Successfully changed password"},status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def userleaveTeam(request):
    user = get_object_or_404(UserProfile, user=request.user)
    teamId = user.teamId
    team = get_object_or_404(TeamRegistration, teamId=teamId)
    user.teamId = None
    user.save()
    team.delete()
    return Response({"message": "You have left the team successfully."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def userjoinTeam(request):
    user = request.user
    teamId = request.data.get('teamId')
    if user is not None:
        user = get_object_or_404(UserProfile, user=user)
        team = get_object_or_404(TeamRegistration, teamId=teamId)
        sport = team.sport
        sport_info = int(sport) 
        if user.teamId.exists():
            if sport_info in [1,2,3,4,5,6,7,8,9,10,11,12] :
                teams=user.teamId.all()
                for team in teams:
                    if int(team.sport) in [1,2,3,4,5,6,7,8,9,10,11,12] :
                        message = "You are not able to join this team"
                        message += "\nYou have to register again to join another team. \nContact Varchas administrators."
                        return Response({"message": message}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
            if sport_info in [13,14,15]:
                teams=user.teamId.all()
                for team in teams:
                    if int(team.sport) == sport_info :
                        message = "You are not able to join this team"
                        message += "\nYou have to register again to join another team. \nContact Varchas administrators."
                        return Response({"message": message}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        # if user.gender != team.captian.gender:
        #     return Response({"message":"Sorry,Gender not matched!"},status=status.HTTP_406_NOT_ACCEPTABLE)
        
        team = get_object_or_404(TeamRegistration, teamId=teamId)
        if(int(team.teamcount) < int(team.teamsize)):
            user.teamId.add(team)
            user.save()
            team.teamcount=team.teamcount+1
            team.save()
            return Response({"message": "Joined team Successfully!"}, status=status.HTTP_201_CREATED)
        else:
           return Response({"message":"Sorry,Team size exceeded!"},status=status.HTTP_406_NOT_ACCEPTABLE)
    return Response({"message": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userDisplayteam(request):
    try:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        team_data = []
        if user_profile.teamId.exists():
            teams = user_profile.teamId.all()
            for team in teams:
                team_users_info = [
                    {
                        "user_id": user_data.user.id,
                        "email": user_data.user.username,
                        "phone": user_data.phone,
                        "name": user_data.user.first_name + user_data.user.last_name
                    }
                    for user_data in UserProfile.objects.filter(teamId=team)
                ]
                team_info = {
                    "team_id": team.teamId,
                    "sport": team.sport,
                    "college": team.college,
                    "captain_username": team.captian.user.first_name + team.captian.user.last_name if team.captian else None,
                    "score": team.score,
                    "category": team.category,
                    "players_info":team_users_info,
                    "captain": team.captian==user_profile
                }
                
                team_data.append(team_info)
        
        if not team_data:
            return Response({"message": "Join a team"}, status=status.HTTP_404_NOT_FOUND)
        
        response_data = {
            "team_data": team_data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userDisplayProfile(request):
    user = get_object_or_404(UserProfile, user=request.user)
    if user is None:
        return Response({"message":"User not found!"},status=status.HTTP_404_NOT_FOUND)
    response_data = {
                "team_id": [team.teamId for team in user.teamId.all()] if user.teamId.exists() else None,
                "college": user.college,
                "user_id": user.user.id,
                "email": user.user.username,
                "phone": user.phone,
                "name":user.user.first_name +user.user.last_name
         }
    return Response(response_data, status=status.HTTP_200_OK)

>>>>>>> 4e91eb38d449294a38a8b441e01997f9bc5d6043
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
