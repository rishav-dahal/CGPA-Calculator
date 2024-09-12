from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager , PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)
    

class User(AbstractBaseUser , PermissionsMixin):
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True, null=True)
    university = models.CharField(max_length=255, null=True)
    college = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def generate_file_name(self, filename):
        extension = filename.split('.')[-1]
        unique_filename = f"{self.email}_{self.id}.{extension}"
        return f'avatars/{unique_filename}'
    
    avatar = models.ImageField(upload_to=generate_file_name, null=True , default='avatars.svg' , blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Subject(models.Model):
    name = models.CharField(max_length=255)
    credit = models.IntegerField()

    class Meta:
        unique_together = ('name', 'credit') 
    
    def __str__(self):
        return self.name
    
class UserSubjectGrade(models.Model):
    GRADE_POINTS = {
        'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'F': 0.0
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)

    class Meta:
        unique_together = ('user', 'subject', 'semester') 

    def grade_point(self):
        return self.GRADE_POINTS.get(self.grade, 0.0)

    def __str__(self):
        return f"{self.user.name} - {self.subject.name} -(SEM:{self.semester.semester_name}) - {self.grade}"
    
class Semester(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='semesters')
    semester_name = models.CharField(max_length=255)
    sgpa = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'semester_name') # user and semester_name should be unique together

    def calculate_sgpa(self):
        user_subject_grades = UserSubjectGrade.objects.filter(semester=self)
        total_credit = 0
        total_grade_point = 0

        # Loop through each grade and calculate the total credits and total grade points
        for grade in user_subject_grades:
            subject_credit = grade.subject.credit
            subject_grade_point = grade.grade_point()  
            total_credit += subject_credit
            total_grade_point += subject_grade_point * subject_credit
        self.sgpa = round(total_grade_point / total_credit, 2) if total_credit > 0 else 0.0
        self.save() 

    def __str__(self):
        return f"{self.user.email} - {self.semester_name} (SGPA: {self.sgpa})"

  
class AggregateResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ,related_name='aggregate_results')  
    cgpa = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_cgpa(self):
        user_subject_grades = UserSubjectGrade.objects.filter(semester__user=self.user)
        total_credit = 0
        total_grade_point = 0

        # Loop through each grade and calculate the total credits and total grade points
        for grade in user_subject_grades:
            subject_credit = grade.subject.credit 
            subject_grade_point = grade.grade_point() 
            total_credit += subject_credit
            total_grade_point += subject_grade_point * subject_credit

        self.cgpa = round(total_grade_point / total_credit, 2) if total_credit > 0 else 0.0
        self.save()

    def __str__(self):
        return f"{self.user.name} - {self.cgpa}"
