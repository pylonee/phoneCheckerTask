from django.db import models

class PhoneRange(models.Model):
    code = models.CharField("ABC\DEF", max_length=40)
    startRange = models.BigIntegerField("От")
    endRange = models.BigIntegerField("До")
    capacity = models.IntegerField("Емкость")
    operator = models.CharField("Оператор", max_length=255)
    region = models.CharField("Регион", max_length=255)
    inn = models.CharField("Инн", max_length=20)
    dateUpdate = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['startRange', 'endRange']),
            models.Index(fields=['operator']),
        ]

    def __str__(self):
        return f"{self.code}: {self.operator} - {self.region}"