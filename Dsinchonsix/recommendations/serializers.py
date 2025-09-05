from teas.models import Tea, TeaCategory
from rest_framework import serializers

#카테고리 조회용
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeaCategory
        fields = ["id", "name", "mood"]

#조회용
class TeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tea
        fields = ["id", "name", "description", "tea_category", "taste", "taste_id"]


#기록용(마셔볼래요 선택 시 디비 저장)
# class LogCreateSerializer(serializers.Serializer):
