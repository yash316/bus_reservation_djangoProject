from django.contrib import admin
from .models import User, Bus, Booking
# Register your models here.

admin.site.register(User)
admin.site.register(Bus)
admin.site.register(Booking)
