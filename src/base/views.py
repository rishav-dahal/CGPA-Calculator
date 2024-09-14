from django.shortcuts import render
from django.http import JsonResponse
from .models import Semester, AggregateResult

def home(request):
    return render(request, 'base/home.html')\

def login(request):
    return render(request, 'base/login.html')

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