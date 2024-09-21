from django.shortcuts import render ,redirect , get_object_or_404
from django.http import JsonResponse
from .models import Semester, AggregateResult , UserSubjectGrade
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UserSubjectGradeForm , SemesterForm

def home(request):
    return render(request, 'base/home.html')\

def loginPage(request):

    page = 'login'
    if request.user.is_authenticated: # is_authenticated is a boolean attribute that will return True if the user is authenticated
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'user does not exist') # messages.error() will display an error message in the template
        
        user = authenticate(request, username=email, password=password) # authenticate() will check if the user exists and if the password is correct

        if user is not None:
            login(request,user) # login() will log in the user
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')

    context = {'page': page}
    return render(request, 'base/login.html',context)


def registerPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('confirm-password')

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        
        try:
            user = User.objects.create_user(email=email, password=password)
            user.save()
            messages.success(request, 'Account was created for ' + email)
            return redirect('login')
        except:
            messages.error(request, 'An error occurred while creating the account')

    return render(request, 'base/register.html')

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    semesters = user.semesters.all()
    aggregate_result, created = AggregateResult.objects.get_or_create(user=user)
    aggregate_result.calculate_cgpa()

    # Collect data for each semester, including subjects, credits, and grades
    semester_data = []
    for semester in semesters:
        subjects = UserSubjectGrade.objects.filter(semester=semester)
        subject_details = [{
            'name': subject.subject.name,
            'credit': subject.subject.credit,
            'grade': subject.grade
        } for subject in subjects]
        semester_data.append({
            'id': semester.id,
            'semester_name': semester.semester_name,
            'subjects': subject_details,
            'sgpa': semester.sgpa
        })

    context = {
        'user': user, # User details
        'semester_data': semester_data, # Details of each semester
        'aggregate_result': aggregate_result, 
    }
    return render(request, 'base/dashboard.html', context)

def add_subject_grade(request, semester_id):
    semester = get_object_or_404(Semester, id=semester_id, user=request.user)

    if request.method == 'POST':
        form = UserSubjectGradeForm(request.POST, user=request.user)  # Pass the user
        if form.is_valid():
            user_subject_grade = form.save(commit=False)
            user_subject_grade.user = request.user
            user_subject_grade.semester = semester
            user_subject_grade.save()

            # Recalculate and update SGPA after adding a grade
            semester.calculate_sgpa()

            return redirect('dashboard')
    else:
        form = UserSubjectGradeForm(user=request.user)  # Pass the user here as well

    context = {
        'form': form,
        'semester': semester
    }
    return render(request, 'base/addsubjectgrade.html', context)

def add_semester(request):
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            semester = form.save(commit=False)
            semester.user = request.user
            semester.save()
            return redirect('dashboard')
    else:
        form = SemesterForm()
    return render(request, 'base/addsemester.html', {'form': form})

# Test API views
def calculate_sgpa_view(request, semester_id):
    try:
        semester = Semester.objects.get(id=semester_id)
        semester.calculate_sgpa()
        return JsonResponse({'message': 'SGPA calculated successfully', 'sgpa': semester.sgpa})
    except Semester.DoesNotExist:
        return JsonResponse({'error': 'Semester not found'}, status=404)

# Test API views
def calculate_cgpa_view(request, user_id):
    try:
        aggregate_result, created = AggregateResult.objects.get_or_create(user_id=user_id)
        aggregate_result.calculate_cgpa()
        return JsonResponse({'message': 'CGPA calculated successfully', 'cgpa': aggregate_result.cgpa})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)