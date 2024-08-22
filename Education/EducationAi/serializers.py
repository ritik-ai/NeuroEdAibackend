from rest_framework import serializers
from .models import user


class RequestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'