from .models import *
from rest_framework import serializers

class Tourserializers(serializers.ModelSerializer):
    Images=serializers.ImageField(required=False)

    class Meta:
        model=Touristplaces
        fields='__all__'