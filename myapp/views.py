from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Car, CarFeature, User
from django.contrib.admin.views.decorators import staff_member_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
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

def about(request):
    return render(request, 'myapp/about.html')

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
def add_car(request):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'Permission denied!'})
    
    if request.method == 'POST':
        name = request.POST.get('name')
        model = request.POST.get('model')
        image = request.FILES.get('image')
        price = request.POST.get('price')
        status = request.POST.get('status')
        description = request.POST.get('description')
        features = request.POST.get('features').split(',')

        car = Car.objects.create(
            name=name,
            model=model,
            image=image,
            price=price.replace('$', '').replace('/day', ''),
            status=status,
            description=description,
            created_by=request.user
        )

        for feature in features:
            CarFeature.objects.create(car=car, feature_name=feature.strip())

        return JsonResponse({'success': True, 'message': 'Car added successfully!'})
    return JsonResponse({'success': False, 'message': 'Invalid request method!'})

@login_required
def edit_car(request, car_id):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'Permission denied!'})
    
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        car.name = request.POST.get('name')
        car.model = request.POST.get('model')
        if 'image' in request.FILES:
            car.image = request.FILES['image']
        car.price = request.POST.get('price').replace('$', '').replace('/day', '')
        car.status = request.POST.get('status')
        car.description = request.POST.get('description')
        car.save()

        # Update features
        car.features.all().delete()
        features = request.POST.get('features').split(',')
        for feature in features:
            CarFeature.objects.create(car=car, feature_name=feature.strip())

        return JsonResponse({'success': True, 'message': 'Car updated successfully!'})
    return JsonResponse({'success': False, 'message': 'Invalid request method!'})

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
