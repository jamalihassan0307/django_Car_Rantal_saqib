from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Main pages
    path('', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Car management
    path('cars/add/', views.add_car, name='add_car'),
    path('cars/edit/<int:car_id>/', views.edit_car, name='edit_car'),
    path('cars/delete/<int:car_id>/', views.delete_car, name='delete_car'),
    path('cars/rent/<int:car_id>/', views.rent_car, name='rent_car'),
    path('cars/return/<int:car_id>/', views.return_car, name='return_car'),
]
