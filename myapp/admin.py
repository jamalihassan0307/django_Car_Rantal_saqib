from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role, Car, CarFeature

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'role')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('profile_picture', 'role')}),
    )

class CarFeatureInline(admin.TabularInline):
    model = CarFeature
    extra = 1

class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'status', 'price', 'created_by', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'model', 'description')
    inlines = [CarFeatureInline]

admin.site.register(User, CustomUserAdmin)
admin.site.register(Role)
admin.site.register(Car, CarAdmin)
admin.site.register(CarFeature)
