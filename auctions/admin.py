from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Listing)
admin.site.register(Comments)
admin.site.register(Bid)