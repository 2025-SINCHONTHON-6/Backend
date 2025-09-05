from rest_framework import serializers
from .models import *
from teas.models import Tea

class ChallengeSerializer(serializers.ModelSerializer):
    # 뷰(View)에서 동적으로 추가해줄 필드들을 미리 정의
    goal = serializers.IntegerField(read_only=True)
    current_progress = serializers.IntegerField(read_only=True)
    is_completed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Challenge
        # 최종 API 응답에 포함될 필드 목록
        fields = [
            'id',
            'title',
            'description',
            'goal',
            'current_progress',
            'is_completed',
        ]


class TeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tea
        fields = ('id', 'name', 'description')

class TeaLogSerializer(serializers.ModelSerializer):
    tea = TeaSerializer(read_only=True)
    tea_id = serializers.PrimaryKeyRelatedField(queryset=Tea.objects.all(), write_only=True, source='tea')

    class Meta:
        model = TeaLogs
        fields = ('id', 'tea', 'tea_id', 'feeling', 'comment', 'created_at')
        read_only_fields = ('id', 'tea', 'created_at')

    def create(self, validated_data):
        return TeaLogs.objects.create(**validated_data)
