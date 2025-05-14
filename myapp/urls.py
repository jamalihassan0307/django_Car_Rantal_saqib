from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.shortcuts import redirect

def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    # Root URL redirects to login
    path('', redirect_to_login, name='home'),
    
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Main pages
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile'),
    
    path('add-car/', views.add_car, name='add_car'),
    path('edit-car/<int:car_id>/', views.edit_car, name='edit_car'),
    path('delete-car/<int:car_id>/', views.delete_car, name='delete_car'),
    path('rent-car/<int:car_id>/', views.rent_car, name='rent_car'),
    path('return-car/<int:car_id>/', views.return_car, name='return_car'),
]
