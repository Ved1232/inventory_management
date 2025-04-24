from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import User  # Changed from auth.User to your custom User model
from django.core.validators import FileExtensionValidator

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, 
                            widget=forms.EmailInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Email'
                            }))
    first_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'First Name'
                                }))
    last_name = forms.CharField(max_length=30, required=True,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Last Name'
                               }))
    phone = forms.CharField(max_length=20, required=False,
                           widget=forms.TextInput(attrs={
                               'class': 'form-control',
                               'placeholder': 'Phone (optional)'
                           }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})
            self.fields[fieldname].help_text = None

class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username or Email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })

class ProfileForm(UserChangeForm):
    password = None  # Remove password field
    
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 
                 'profile_image', 'phone', 'address']
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True