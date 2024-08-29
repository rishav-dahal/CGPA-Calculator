from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True, null=True)
    university = models.CharField(max_length=255, null=True)
    college = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_file_name(self, filename):
        extension = filename.split('.')[-1]
        unique_filename = f"{self.email}_{self.id}.{extension}"
        return f'avatars/{unique_filename}'
    
    avatar = models.ImageField(upload_to=generate_file_name, null=True , default='avatars.svg' blank=True)

    def grade_point(self):
        grade_conversion = {
            'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D+': 1.3, 'D': 1.0, 'F': 0.0
        }
        return grade_conversion.get(self.grade, 0.0) # 0.0 is default value
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name

class Semester(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    semester = models.CharField(max_length=255)
    subjects = models.ManyToManyField('Subject')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_sgpa(self):
        total_credit = sum([subject.credit for subject in self.subjects.all()])
        total_grade_point = sum(subject.grade_point * subject.credit for subject in self.subjects.all())
        return round(total_grade_point / total_credit, 2) if total_credit> 0 else 0.0 

    def __str__(self):
        return f"{self.user.name} - {self.semester}"

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
        return f"{self.semester} - {self.sgpa}"
    
class AggregateResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cgpa = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_cgpa(self):
        results = Result.objects.filter(semester__user=self.user)
        total_sgpa = sum(result.sgpa for result in results)
        self.cgpa = round(total_sgpa / results.count(), 2) if results.count() > 0 else 0.0
        self.save()

    def __str__(self):
        return f"{self.user.name} - {self.cgpa}"
