from django.contrib import admin
from .models import Car

class CarAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'year', 'category', 'available')
    list_filter = ('category', 'available')
    search_fields = ('title', 'features')
    list_editable = ('available',)

admin.site.register(Car, CarAdmin)