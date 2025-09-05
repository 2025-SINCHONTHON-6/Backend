from django.db import models
from django.conf import settings

class Challenge(models.Model):
    # 챌린지 종류를 코드로 구분하기 위한 상수
    class ChallengeType(models.TextChoices):
        DRINK_COUNT = 'DRINK_COUNT', '추천 차 마시기 횟수'
        RECORD_COUNT = 'RECORD_COUNT', '기록 작성 횟수'
        UNIQUE_TEA_COUNT = 'UNIQUE_TEA_COUNT', '서로 다른 종류의 차 마시기'
        CONSECUTIVE_DAYS = 'CONSECUTIVE_DAYS', '연속으로 차 마시기'

    title = models.CharField(max_length=100, verbose_name="챌린지 제목")
    description = models.TextField(verbose_name="챌린지 설명")
    
    challenge_type = models.CharField(
        max_length=50, 
        choices=ChallengeType.choices, 
        verbose_name="챌린지 종류"
    )

    def __str__(self):
        return self.title

class TeaLogs(models.Model):
    id = models.BigAutoField(primary_key=True)
    tea = models.ForeignKey('teas.Tea', on_delete=models.CASCADE, null=False, verbose_name="차 아이디")  # ← 중요
    created_at = models.DateField(auto_now_add=True, verbose_name="차 마신 날짜")
    feeling = models.CharField(max_length=30, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.tea) + " - " + str(self.created_at)

class RecentRecommendedTea(models.Model):
    tea = models.ForeignKey('teas.Tea', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)