from django.shortcuts import render ,redirect
from django.http import JsonResponse
from .models import Semester, AggregateResult
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import User
from django.contrib.auth import logout

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