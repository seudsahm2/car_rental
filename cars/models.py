from django.db import models

class Car(models.Model):
    CATEGORY_CHOICES = [
        ('LUXURY', 'Luxury'),
        ('SPORTS', 'Sports'),
        ('SUV', 'SUV'),
        ('CONVERTIBLE', 'Convertible'),
    ]
    
    title = models.CharField(max_length=200)
    image = models.URLField(max_length=500)
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