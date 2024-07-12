from django.urls import path
from . import views

urlpatterns = [
    # Customer related paths
    path("", views.customer_login, name="customer_login"),  # Customer login page
    path("signup/", views.customer_signup, name="customer_signup"),  # Customer signup page
    path("home/", views.customer_home, name="customer_home"),  # Customer home page
    path("servicecall/", views.customer_service_call, name="customer_service_call"),  # Page to create a service call
    path('accept/<int:service_call_id>/', views.customer_accept, name='customer_accept'),  # Accept a service call
    path('accept_response/<int:response_id>/', views.accept_response, name='accept_response'),  # Accept a service provider's response

    # Customer progression and approval paths
    path('progression/<int:accepted_id>/', views.customer_progression, name='customer_progression'),  # View service progression
    path('approve_service/<int:accepted_id>/', views.customer_approve_service, name='customer_approve_service'),  # Approve service completion
    path('approve_payment/<int:accepted_id>/', views.customer_approve_payment, name='customer_approve_payment'),  # Approve payment completion
    path('service_done/<int:accepted_id>/', views.customer_service_done, name='customer_service_done'),  # Mark service as done

    path("logout/", views.customer_logout, name="customer_logout"),  # Customer logout

    # Service provider related paths
    path("service/", views.service_login, name="service_provider_login"),  # Service provider login page
    path("service/signup/", views.service_signup, name="service_provider_signup"),  # Service provider signup page
    path("service/home/", views.service_home, name="service_provider_home"),  # Service provider home page
    path("service/response2call/", views.service_response_to_call, name="service_provider_response_to_call"),  # Page to respond to service calls
    path("service/response/", views.service_response, name="service_provider_response"),  # Submit response to a service call
    
    # Service provider progression and approval paths
    path('service/progression/<int:accepted_id>/', views.service_progression, name='service_provider_progression'),  # View service progression
    path('service/approve_service/<int:accepted_id>/', views.service_approve_service, name='service_provider_approve_service'),  # Approve service completion
    path('service/approve_payment/<int:accepted_id>/', views.service_approve_payment, name='service_provider_approve_payment'),  # Approve payment completion
    path('service/service_done/<int:accepted_id>/', views.service_service_done, name='service_provider_service_done'),  # Mark service as done
    
    path('service/progression/<int:accepted_id>/update-venue-reached/', views.update_venue_reached, name='update_venue_reached'),  # Update venue reached status

    path("service/logout/", views.service_logout, name="service_provider_logout"),  # Service provider logout
]
