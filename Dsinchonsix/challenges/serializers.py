from rest_framework import serializers
from .models import Challenge

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