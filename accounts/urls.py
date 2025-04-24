from django.urls import path
from .views import (
    SignUpView, 
    CustomLoginView,
    CustomLogoutView,
    ProfileView,
    AdminDashboardView,
     ProfileUpdateView,
    manage_users
)
from django.contrib.auth.views import LogoutView
app_name = 'accounts'

urlpatterns = [
    # Authentication URLs
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
    # Profile Management
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # Role-based Access URLs
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('manage-users/', manage_users, name='manage_users'),

    
]