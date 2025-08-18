from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(models.Model):
    userId = models.CharField(max_length=100, unique=True) # userId, groupId, roomId
    userType = models.CharField(max_length=10) # user or group or room
    grade = models.IntegerField(validators=[MinValueValidator(limit_value=1), MaxValueValidator(limit_value=6)]) # 1-6年生
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "A " + str(self.grade) + "th grade student joined at" + str(self.created_at)