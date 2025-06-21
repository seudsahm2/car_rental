from django.db import models
from django.utils.html import format_html

class Car(models.Model):
    CATEGORY_CHOICES = [
        ('LUXURY', 'Luxury'),
        ('SPORTS', 'Sports'),
        ('SUV', 'SUV'),
        ('CONVERTIBLE', 'Convertible'),
    ]
    
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    price = models.CharField(max_length=50)
    year = models.CharField(max_length=10)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    features = models.JSONField(default=list)
    whatsapp_number = models.CharField(max_length=20, default='+1234567890')
    call_number = models.CharField(max_length=20, default='+1234567890')
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_preview(self):
        if self.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', self.image.url)
        elif self.image_url:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', self.image_url)
        return "No Image"
    image_preview.short_description = 'Preview'