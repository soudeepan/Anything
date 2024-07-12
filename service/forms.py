from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.forms.widgets import PasswordInput, TextInput
from django import forms
from .models import *

# Form to create a new customer
class CreateCustomerForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    contact_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'contact_number']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            customer = Customer(
                user=user,
                contact_number=self.cleaned_data['contact_number']
            )
            customer.save()
            customer_group = Group.objects.get(name='Customer')
            user.groups.add(customer_group)
        return user

# Form to create a new service provider
class CreateServiceProviderForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    contact_number = forms.CharField(max_length=15, required=True)
    service_category = forms.ChoiceField(choices=SERVICE_CATEGORIES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'contact_number', 'password1', 'password2', 'service_category']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            service_provider = ServiceProvider(
                user=user, 
                contact_number=self.cleaned_data['contact_number'], 
                service_category=self.cleaned_data['service_category']
            )
            service_provider.save()
            service_provider_group = Group.objects.get(name='Service Provider')
            user.groups.add(service_provider_group)
        return user

# Login form for customers
class CustomerLoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    def confirm_login_allowed(self, user):
        if not user.groups.filter(name='Customer').exists():
            raise forms.ValidationError("This user is not a customer.", code='invalid_login')

# Login form for service providers
class ServiceProviderLoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    def confirm_login_allowed(self, user):
        if not user.groups.filter(name='Service Provider').exists():
            raise forms.ValidationError("This user is not a service provider.", code='invalid_login')

# Form to create a new service call
class ServiceCallForm(forms.ModelForm):
    category = forms.ChoiceField(choices=SERVICE_CATEGORIES, required=True, help_text='Category')

    class Meta:
        model = ServiceCall
        fields = ['category', 'description', 'location', 'time']
        widgets = {
            'time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
