from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify

class CarCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Car Categories"

class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    category = models.ForeignKey(CarCategory, on_delete=models.SET_NULL, null=True, related_name='cars')
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    seats = models.PositiveIntegerField(default=4)
    insurance_included = models.BooleanField(default=False)
    usdt_accepted = models.BooleanField(default=False)
    whatsapp_deal = models.BooleanField(default=False)
    no_security_deposit = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    luggage_capacity = models.PositiveIntegerField(default=2)
    doors = models.PositiveIntegerField(default=2)
    passengers = models.PositiveIntegerField(default=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=3000.00)
    mileage_limit = models.PositiveIntegerField(default=250)
    additional_km_rate = models.CharField(max_length=50, default="AED 5 – AED 30")
    is_active = models.BooleanField(default=True)
    location_content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    location_object_id = models.PositiveIntegerField(null=True, blank=True)
    location = GenericForeignKey('location_content_type', 'location_object_id')

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            base_slug = slugify(f"{self.make}-{self.model}-{self.year}")
            super().save(*args, **kwargs)
            self.slug = f"{base_slug}-{self.id}"
            super().save(update_fields=['slug'])
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

class ImageGallery(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='gallery_images')
    image_path = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=100, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.is_primary:
            # Unset is_primary for other images of the same car
            ImageGallery.objects.filter(car=self.car, is_primary=True).exclude(id=self.id).update(is_primary=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.car.make} {self.car.model}"

    class Meta:
        ordering = ['-is_primary', 'order']  # Primary image first, then by order
        constraints = [
            models.UniqueConstraint(
                fields=['car', 'is_primary'],
                condition=models.Q(is_primary=True),
                name='unique_primary_image_per_car'
            )
        ]

class MaintenanceLog(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100)
    service_date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.service_type} for {self.car.make} {self.car.model}"

    class Meta:
        ordering = ['-service_date']
class PricingTier(models.Model):  
    name = models.CharField(max_length=50)  
    description = models.TextField(blank=True)  
    multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)  
    is_active = models.BooleanField(default=True)  
    
    def __str__(self):
        return f"{self.name} (x{self.multiplier})"