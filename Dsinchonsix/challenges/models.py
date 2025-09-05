from django.db import models

class TeaLogs(models.Model):
    id = models.BigAutoField(primary_key=True)
    tea_id = models.ForeignKey('teas.Tea', on_delete=models.CASCADE, null=False, verbose_name="차 아이디")
    date = models.DateField(auto_now_add=True, verbose_name="차 마신 날짜")

    def __str__(self):
        return str(self.tea_id)