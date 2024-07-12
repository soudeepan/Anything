from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import *

# Customer Signup View
def customer_signup(request):
    form = forms.CreateCustomerForm()

    if request.method == 'POST':
        form = forms.CreateCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_login')  # Redirect to customer login after successful signup

    context = {'signupform': form}
    return render(request, 'service/signup.html', context=context)

# Customer Login View
def customer_login(request):
    form = forms.CustomerLoginForm()

    if request.method == 'POST':
        form = forms.CustomerLoginForm(request, data=request.POST)
        if form.is_valid():    
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None and user.groups.filter(name='Customer').exists():
                login(request, user)
                return redirect('customer_home')  # Redirect to customer home if login is successful
            else:
                form.add_error(None, 'Invalid login credentials or not a customer.')

    context = {'loginform': form}
    return render(request, 'service/login.html', context=context)

# Customer Logout View
def customer_logout(request):
    logout(request)
    return redirect('customer_login')  # Redirect to customer login after logout

# Customer Home View
@login_required
def customer_home(request):
    try:
        customer = Customer.objects.get(user=request.user)
        service_calls = ServiceCall.objects.filter(customer_id=customer.id)
        accepted_service_calls = Accepted.objects.filter(customer_id=customer)
        
        for call in service_calls:
            print(f"ServiceCall ID: {call.id}, Category: {call.category}, Time: {call.time.timestamp() if call.time else 'No time'}, Customer ID: {call.customer_id}")

    except Customer.DoesNotExist:
        service_calls = []

    context = {
        'user': request.user,
        'service_calls': service_calls,
        'accepted_service_calls': accepted_service_calls,
    }
    return render(request, 'service/home.html', context)

# Create Service Call View for Customer
@login_required
def customer_service_call(request):
    if request.method == 'POST':
        form = forms.ServiceCallForm(request.POST)
        if form.is_valid():
            service_call = form.save(commit=False)
            service_call.customer_id = Customer.objects.get(user=request.user)
            service_call.save()
            return redirect('customer_home')  # Redirect to customer home after creating a service call
        else:
            print("Form is not valid:", form.errors) 
    else:
        form = forms.ServiceCallForm()

    context = {
        'form': form
    }
    return render(request, 'service/servicecall.html', context)

# Accept Service Call View for Customer
@login_required
def customer_accept(request, service_call_id):
    service_call = get_object_or_404(ServiceCall, id=service_call_id)
    response_calls = ResponseCall.objects.filter(service_id=service_call)

    context = {
        'service_call': service_call,
        'response_calls': response_calls,
    }
    
    return render(request, 'service/accept.html', context)

# Accept Response Call View for Customer
@login_required
def accept_response(request, response_id):
    response = get_object_or_404(ResponseCall, id=response_id)
    service_call = response.service_id

    accepted = Accepted.objects.create(
        customer_id=service_call.customer_id,
        customer_contact=service_call.customer_id.contact_number,
        customer_name=f"{service_call.customer_id.user.first_name} {service_call.customer_id.user.last_name}",
        service_provider_id=response.service_provider_id,
        service_provider_contact=response.service_provider_id.contact_number,
        service_provider_name=f"{response.service_provider_id.user.first_name} {response.service_provider_id.user.last_name}",
        location=service_call.location,
        time=service_call.time,
        category=service_call.category,
        problem=service_call.description,
        cost=response.cost,
        time_taken=response.time_taken,
    )

    service_call.delete()  # Delete the service call after it has been accepted

    return redirect('customer_home')

# View Service Progression for Customer
@login_required
def customer_progression(request, accepted_id):
    accepted_service = get_object_or_404(Accepted, id=accepted_id, customer_id=request.user.customer)

    context = {
        'accepted_service': accepted_service,
    }
    
    return render(request, 'service/progression.html', context)

# Approve Service by Customer
@login_required
def customer_approve_service(request, accepted_id):
    accepted_service = get_object_or_404(Accepted, id=accepted_id, customer_id=request.user.customer)
    accepted_service.service_approval_customer = True
    accepted_service.save()
    return redirect('customer_progression', accepted_id=accepted_id)

# Approve Payment by Customer
@login_required
def customer_approve_payment(request, accepted_id):
    accepted_service = get_object_or_404(Accepted, id=accepted_id, customer_id=request.user.customer)
    accepted_service.payment_approval_customer = True
    accepted_service.save()
    return redirect('customer_progression', accepted_id=accepted_id)

# Mark Service as Done for Customer
@login_required
def customer_service_done(request, accepted_id):
    accepted_service = get_object_or_404(Accepted, id=accepted_id, customer_id=request.user.customer)   
    if accepted_service.venue_reached and accepted_service.service_provided and accepted_service.payment_received:
        accepted_service.delete()  # Delete the record if service is done and payment is received
        return redirect('customer_home')
    else:
        return redirect('customer_home')

# Service Provider Signup View
def service_signup(request):
    form = forms.CreateServiceProviderForm()

    if request.method == 'POST':
        form = forms.CreateServiceProviderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_provider_login')  # Redirect to service provider login after successful signup

    context = {'signupform': form}
    return render(request, 'service/sp_signup.html', context=context)

# Service Provider Login View
def service_login(request):
    form = forms.ServiceProviderLoginForm()

    if request.method == 'POST':
        form = forms.ServiceProviderLoginForm(request, data=request.POST)
        if form.is_valid():    
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None and user.groups.filter(name='Service Provider').exists():
                login(request, user)
                return redirect('service_provider_home')  # Redirect to service provider home if login is successful
            else:
                form.add_error(None, 'Invalid login credentials or not a service provider.')

    context = {'loginform': form}
    return render(request, 'service/sp_login.html', context=context)

# Service Provider Logout View
def service_logout(request):
    logout(request)
    return redirect('service_provider_login')  # Redirect to service provider login after logout

# Service Provider Home View
@login_required
def service_home(request):
    service_provider = request.user
    service_provider_instance = ServiceProvider.objects.get(user=service_provider)
    category = service_provider_instance.service_category
    service_calls_same = ServiceCall.objects.filter(category=category)
    service_calls_diff = ServiceCall.objects.exclude(category=category)
    accepted_service_calls = Accepted.objects.filter(service_provider_id=service_provider_instance)

    context = {
        'service_provider': service_provider,
        'service_calls_same': service_calls_same,
        'service_calls_diff': service_calls_diff,
        'accepted_service_calls': accepted_service_calls,
    }
    return render(request, 'service/sp_home.html', context=context)

# Service Provider Response to Call View
@login_required
def service_response_to_call(request):
    cost = request.POST.get('cost')
    time_taken = request.POST.get('time_taken')
    call_id = request.POST.get('call_id')
    
    if cost and time_taken and call_id:
        try:
            call = ServiceCall.objects.get(id=call_id)
            ResponseCall.objects.create(
                service_id=call,
                service_provider_id=ServiceProvider.objects.get(user=request.user),
                cost=cost,
                time_taken=time_taken,
            )
        except ServiceCall.DoesNotExist:
            pass
    
    return redirect('service_provider_home')  # Redirect to service provider home after responding to a call

# View Service Provider's Responses
@login_required
def service_response(request):
    service_provider = get_object_or_404(ServiceProvider, user=request.user)
    response_calls = ResponseCall.objects.filter(service_provider_id=service_provider)
    responded_service_call_ids = response_calls.values_list('service_id', flat=True)
    responded_service_calls = []
    
    for service_call_id in responded_service_call_ids:
        service_call = get_object_or_404(ServiceCall, id=service_call_id)
        response_call = ResponseCall.objects.filter(service_id=service_call_id, service_provider_id=service_provider).first()
        responded_service_calls.append((service_call, response_call))
    
    context = {
        'service_provider': service_provider,
        'responded_service_calls': responded_service_calls,
    }
    
    return render(request, 'service/sp_response.html', context=context)

# View Service Progression for Service Provider
@login_required
def service_progression(request, accepted_id):
    accepted_service = get_object_or_404(Accepted, id=accepted_id, service_provider_id=request.user.serviceprovider)

    context = {
        'accepted_service': accepted_service,
    }
    
    return render(request, 'service/sp_progression.html', context)

# Approve Service by Service Provider
@login_required
def service_approve_service(request, accepted_id):
    accepted_service = get_object_or_404(Accepted, id=accepted_id, service_provider_id=request.user.serviceprovider)
    accepted_service.service_approval_service_provider = True
    accepted_service.save()
    return redirect('service_provider_progression', accepted_id=accepted_id)

# Approve Payment by Service Provider
@login_required
def service_approve_payment(request, accepted_id):
    accepted_service = get_object_or_404(Accepted, id=accepted_id, service_provider_id=request.user.serviceprovider)
    accepted_service.payment_approval_service_provider = True
    accepted_service.save()
    return redirect('service_provider_progression', accepted_id=accepted_id)

# Mark Service as Done for Service Provider
@login_required
def service_service_done(request, accepted_id):
    accepted_service = get_object_or_404(Accepted, id=accepted_id, service_provider_id=request.user.serviceprovider)   
    if accepted_service.venue_reached and accepted_service.service_provided and accepted_service.payment_received:
        accepted_service.delete()  # Delete the record if service is done and payment is received
        return redirect('service_provider_home')
    else:
        return redirect('service_provider_home')

# Update Venue Reached Status for Service Provider
@require_POST
@login_required
def update_venue_reached(request, accepted_id):
    accepted_service = get_object_or_404(Accepted, id=accepted_id, service_provider_id=request.user.serviceprovider)
    
    if not accepted_service.venue_reached:
        accepted_service.venue_reached = True
        accepted_service.save()

    return redirect('service_provider_progression', accepted_id=accepted_id)
