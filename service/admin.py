from django.contrib import admin
from . models import *

admin.site.register(Customer)
admin.site.register(ServiceProvider)
admin.site.register(ServiceCall)
admin.site.register(ResponseCall)
admin.site.register(Accepted)