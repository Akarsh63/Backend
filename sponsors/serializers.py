<<<<<<< HEAD
=======
from .models import Sponsor,SponsorType
>>>>>>> 4e91eb38d449294a38a8b441e01997f9bc5d6043
from rest_framework import serializers
from .models import Sponsor,SponsorType

<<<<<<< HEAD
class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['name', 'sponsor_type', 'link', 'logo']

class SponsorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SponsorType
=======

class SponsorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SponsorType
        fields = ['name','order']

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
>>>>>>> 4e91eb38d449294a38a8b441e01997f9bc5d6043
        fields = '__all__'
