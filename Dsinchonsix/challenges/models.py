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

class UserChallenge(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='challenges'
    )
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False, verbose_name="완료 여부")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="완료일")

    class Meta:
        unique_together = ('user', 'challenge')

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title} ({'완료' if self.is_completed else '진행중'})"

class TeaLogs(models.Model):
    id = models.BigAutoField(primary_key=True)
    tea_id = models.ForeignKey('teas.Tea', on_delete=models.CASCADE, null=False, verbose_name="차 아이디")
    date = models.DateField(auto_now_add=True, verbose_name="차 마신 날짜")

    def __str__(self):
        return str(self.tea_id) + " - " + str(self.date)
