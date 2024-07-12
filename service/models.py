from django.db import models
from django.contrib.auth.models import User

# Service categories options
SERVICE_CATEGORIES = [
    ('Plumbing', 'Plumbing'),
    ('Electrical', 'Electrical'),
    ('Cleaning', 'Cleaning'),
    ('Gardening', 'Gardening'),
    ('Painting', 'Painting'),
    ('Carpentry', 'Carpentry'),
    ('HVAC', 'HVAC'),
    ('Pest Control', 'Pest Control'),
    ('Landscaping', 'Landscaping'),
    ('Roofing', 'Roofing'),
    ('Appliance Repair', 'Appliance Repair'),
    ('Home Cleaning', 'Home Cleaning'),
    ('Water Purifier Service', 'Water Purifier Service'),
    ('Salon at Home', 'Salon at Home'),
    ('Pest Control', 'Pest Control'),
    ('AC Service', 'AC Service'),
    ('Water Tank Cleaning', 'Water Tank Cleaning'),
    ('Internet Installation', 'Internet Installation'),
    ('Geyser Repair', 'Geyser Repair'),
]

# Customer model to store customer information
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

# ServiceProvider model to store service provider information
class ServiceProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    service_category = models.CharField(max_length=50, choices=SERVICE_CATEGORIES)

    def __str__(self):
        return self.user.username

# ServiceCall model to store details of service calls made by customers
class ServiceCall(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='service_calls')
    category = models.CharField(max_length=50, choices=SERVICE_CATEGORIES)
    description = models.TextField()
    location = models.CharField(max_length=255)
    time = models.DateTimeField()

    def __str__(self):
        return f'Service Call by {self.customer_id.user.username} for {self.category} on {self.time}'

# ResponseCall model to store responses to service calls by service providers
class ResponseCall(models.Model):
    service_id = models.ForeignKey(ServiceCall, on_delete=models.CASCADE, related_name='response_calls')
    service_provider_id = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='service_providers')
    cost = models.DecimalField(max_digits=10, decimal_places=2, help_text='Cost in rupees')
    time_taken = models.DecimalField(max_digits=5, decimal_places=2, help_text='Time taken in hours')

    def __str__(self):
        return f"Response for Service ID: {self.service_id.id} by Provider ID: {self.service_provider_id.id}"

# Accepted model to store details of accepted service calls
class Accepted(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer_contact = models.CharField(max_length=15)
    customer_name = models.CharField(max_length=255)
    service_provider_id = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    service_provider_contact = models.CharField(max_length=15)
    service_provider_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    time = models.DateTimeField()
    category = models.CharField(max_length=50, choices=SERVICE_CATEGORIES)
    problem = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, help_text='Cost in rupees')
    time_taken = models.DecimalField(max_digits=5, decimal_places=2, help_text='Time taken in hours')

    # Approval and status fields
    service_approval_customer = models.BooleanField(default=False)
    service_approval_service_provider = models.BooleanField(default=False)
    payment_approval_customer = models.BooleanField(default=False)
    payment_approval_service_provider = models.BooleanField(default=False)
    venue_reached = models.BooleanField(default=False)
    service_provided = models.BooleanField(default=False)
    payment_received = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Update status based on approvals
        if self.service_approval_customer and self.service_approval_service_provider:
            self.service_provided = True
        if self.payment_approval_customer and self.payment_approval_service_provider:
            self.payment_received = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Accepted Service by {self.customer_name} with {self.service_provider_name}"
