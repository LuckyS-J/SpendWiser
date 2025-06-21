from django.db import models
from core.models import CustomUser

# Create your models here.

class Goal(models.Model):
  user = models.ForeignKey(CustomUser, related_name='goals', on_delete=models.CASCADE)
  name = models.CharField(max_length=150)
  target = models.IntegerField()
  current = models.IntegerField()
  created_at = models.DateField(auto_now=True)

  def __str__(self):
    return f"{self.name}, {self.user.username}"
  
  @property
  def is_completed(self):
    return self.current >= self.target