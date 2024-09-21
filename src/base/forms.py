from .models import User , UserSubjectGrade , Semester
from django.contrib.auth.forms import UserCreationForm
from django import forms

# Form for adding a subject and its grade to a specific semester
class UserSubjectGradeForm(forms.ModelForm):
    class Meta:
        model = UserSubjectGrade
        fields = ['subject', 'grade']
        widgets = {
            'subject': forms.Select(attrs={'class': 'select2'})  # Use Select2 widget for better UX
        }

    def __init__(self, *args, **kwargs):
        """
        Customizes the form to show only available subjects for the selected semester.
        """
        # Pop user and semester from kwargs to pass it to form instance
        self.user = kwargs.pop('user', None)
        self.semester = kwargs.pop('semester', None)
        super(UserSubjectGradeForm, self).__init__(*args, **kwargs)

        # Filter subjects based on the selected semester and user
        if self.semester and self.user:
            self.fields['subject'].queryset = self.fields['subject'].queryset.filter(
                semester=self.semester, user=self.user
            )

    def save(self, commit=True):
        """
        Override the save method to auto-fill user and semester.
        """
        instance = super(UserSubjectGradeForm, self).save(commit=False)
        instance.user = self.user
        instance.semester = self.semester
        if commit:
            instance.save()
        return instance

# Form for adding a new semester
class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['semester_name']  # Only include the semester name as a field
