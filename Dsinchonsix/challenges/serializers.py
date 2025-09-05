from rest_framework import serializers
from .models import *
from teas.models import Tea

class TeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tea
        fields = ('id', 'name')

class TeaLogSerializer(serializers.ModelSerializer):
    tea = TeaSerializer(read_only=True)
    tea_id = serializers.PrimaryKeyRelatedField(queryset=Tea.objects.all(), write_only=True, source='tea')

    class Meta:
        model = TeaLogs
        fields = ('id', 'tea', 'tea_id', 'feeling', 'comment', 'created_at')
        read_only_fields = ('id', 'tea', 'created_at')