from rest_framework import serializers
from .models import Sponsor,SponsorType

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['name', 'sponsor_type', 'link', 'logo']

class SponsorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SponsorType
        fields = '__all__'
