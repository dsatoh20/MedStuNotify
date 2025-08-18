from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Lecture(models.Model):
    grade = models.IntegerField(validators=[MinValueValidator(limit_value=1), MaxValueValidator(limit_value=6)])  # 1-6年生
    subject = models.CharField(max_length=200) # 科目名
    content = models.TextField()  # 変更内容
    created_at = models.DateTimeField(auto_now_add=True)  # 読み込み日時

    def __str__(self):
        return f"{self.grade}th grade {self.subject} (posted at {self.created_at.date()})"