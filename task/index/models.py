from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    question = models.CharField(max_length=100,null=True)
    op1 = models.CharField(max_length=100,null=True)
    op2 = models.CharField(max_length=100,null=True)
    op3 = models.CharField(max_length=100,null=True)
    op4 = models.CharField(max_length=100,null=True)
    ans = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.question
    
class Result(models.Model):
    user=models.ForeignKey(User,on_delete=User)
    result=models.CharField(max_length=100)
    def __str__(self):
        return str(self.user)
