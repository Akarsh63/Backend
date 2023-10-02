from django.views.generic import ListView
from .models import SponsorType, Sponsor
from accounts.models import EsportsUserProfile, UserProfile
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, permissions,status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SponsorSerializer


class SponsorView(ListView):
    model = SponsorType

    template_name = 'sponsors/index.html'

    def get_context_data(self, **kwargs):
        if self.request.user.username != "":
            try:
                userprofile = get_object_or_404(UserProfile, user=self.request.user)
            except:
                userprofile = get_object_or_404(EsportsUserProfile, user=self.request.user)
        context = super(SponsorView, self).get_context_data(**kwargs)
        if self.request.user.username != "":
            context['userprofile'] = userprofile
            context['page'] = "home"
        return context
@api_view(['GET'])
def get_all_sponsors(request):
    sponsors = Sponsor.objects.all()
    serializer = SponsorSerializer(sponsors, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

class SponsorViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [permissions.AllowAny]
