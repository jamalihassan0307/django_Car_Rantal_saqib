from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Car, CarFeature, User
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CarForm
from django.contrib.sessions.backends.db import SessionStore

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Create session
            session = SessionStore()
            session.create()
            session['user_id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            session['is_authenticated'] = True
            session.save()
            
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password!')
    return render(request, 'myapp/index.html')

@login_required
def dashboard(request):
    cars = Car.objects.all()
    context = {
        'cars': cars,
        'is_admin': request.user.is_staff,
        'is_superuser': request.user.is_superuser
    }
    return render(request, 'myapp/dashboard.html', context)

@login_required
def about(request):
    return render(request, 'myapp/about.html')

@login_required
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Here you can add logic to handle the contact form submission
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')
    return render(request, 'myapp/contact.html')

@login_required
@staff_member_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.created_by = request.user
            car.save()
            
            # Handle features
            features = request.POST.get('features', '').split(',')
            for feature in features:
                feature = feature.strip()
                if feature:
                    CarFeature.objects.create(car=car, feature_name=feature)
            
            messages.success(request, 'Car added successfully!')
            return redirect('dashboard')
    else:
        form = CarForm()
    
    return render(request, 'myapp/car_form.html', {
        'form': form,
        'title': 'Add New Car',
        'submit_text': 'Add Car'
    })

@login_required
@staff_member_required
def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            car = form.save()
            
            # Handle features
            car.features.all().delete()
            features = request.POST.get('features', '').split(',')
            for feature in features:
                feature = feature.strip()
                if feature:
                    CarFeature.objects.create(car=car, feature_name=feature)
            
            messages.success(request, 'Car updated successfully!')
            return redirect('dashboard')
    else:
        form = CarForm(instance=car)
        # Pre-populate features field
        form.initial['features'] = ', '.join([f.feature_name for f in car.features.all()])
    
    return render(request, 'myapp/car_form.html', {
        'form': form,
        'title': 'Edit Car',
        'submit_text': 'Update Car',
        'car': car
    })

@login_required
def delete_car(request, car_id):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'Permission denied!'})
    
    car = get_object_or_404(Car, id=car_id)
    car.delete()
    return JsonResponse({'success': True, 'message': 'Car deleted successfully!'})

@login_required
def rent_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if car.status == 'available':
        car.status = 'rented'
        car.save()
        return JsonResponse({'success': True, 'message': 'Car rented successfully!'})
    return JsonResponse({'success': False, 'message': 'Car is not available!'})

@login_required
def return_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if car.status == 'rented':
        car.status = 'available'
        car.save()
        return JsonResponse({'success': True, 'message': 'Car returned successfully!'})
    return JsonResponse({'success': False, 'message': 'Car is not rented!'})

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'myapp/profile.html', {'user': request.user})

def logout_view(request):
    if request.user.is_authenticated:
        # Clear the session
        request.session.flush()
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')

