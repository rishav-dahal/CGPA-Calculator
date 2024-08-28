from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True, null=True)
    university = models.CharField(max_length=255, null=True)
    college = models.CharField(max_length=255, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True , default='avatars/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Semester(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    semester = models.CharField(max_length=255)
    subjects = models.ManyToManyField('Subject')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.semester 

class Subject(models.Model):
    name = models.CharField(max_length=255)
    credit = models.IntegerField()
    grade = models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Result(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    sgpa = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.cgpa)
    
class AggregateResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cgpa = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.cgpa)
