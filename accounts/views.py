from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import SignUpForm, LoginForm, ProfileForm
from .models import User
from django.views import View
from .decorators import role_required

class SignUpView(CreateView):
    """Handles user registration with default role assignment"""
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = 'staff'  # Set default role
        user.save()
        messages.success(self.request, 'Account created successfully! Please log in.')
        return super().form_valid(form)

class CustomLoginView(LoginView):
    """Custom login view with role-based redirection"""
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        user = form.get_user()
        welcome_message = f'Welcome back, {user.get_full_name() or user.username}!'
        messages.success(self.request, welcome_message)
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect users based on their role"""
        role_redirects = {
            'admin': 'admin_dashboard',
            'manager': 'manager_dashboard'
        }
        return reverse_lazy(role_redirects.get(self.request.user.role, 'dashboard'))

class ProfileView(LoginRequiredMixin, UpdateView):
    """Handles user profile updates"""
    model = User
    form_class = ProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Handles user profile editing"""
    model = User
    form_class = ProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)
    
class RoleRestrictedView(LoginRequiredMixin):
    """Base view for role-based access control"""
    allowed_roles = []
    permission_denied_message = "You don't have permission to access this page."
    redirect_url = 'dashboard'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.role not in self.allowed_roles:
            messages.error(request, self.permission_denied_message)
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)

class AdminDashboardView(RoleRestrictedView, TemplateView):
    """Admin-specific dashboard view"""
    allowed_roles = ['admin']
    template_name = 'accounts/admin_dashboard.html'
    permission_denied_message = "Admin privileges required to access this page."

class ManagerDashboardView(RoleRestrictedView, TemplateView):
    """Manager-specific dashboard view"""
    allowed_roles = ['manager', 'admin']  # Admins can also access manager views
    template_name = 'accounts/manager_dashboard.html'
    permission_denied_message = "Manager privileges required to access this page."

@role_required('admin', 'manager')
def manage_users(request):
    """User management view for admins and managers"""
    users = User.objects.all().order_by('date_joined')
    context = {
        'users': users,
        'total_users': users.count()
    }
    return render(request, 'accounts/manage_users.html', context)

class CustomLogoutView(LoginRequiredMixin, View):
    """Custom logout view with message and redirection"""
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect('accounts:login')