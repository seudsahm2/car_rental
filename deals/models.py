from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify

class MonthlyRentalDeal(models.Model):
    # Use GenericForeignKey to avoid direct dependency on `fleet.Car`
    car_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    car_object_id = models.PositiveIntegerField()
    car = GenericForeignKey('car_content_type', 'car_object_id')
    discount_percentage = models.PositiveIntegerField(default=0)
    monthly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    promo_tag = models.CharField(max_length=50, blank=True)
    terms = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.car.make} {self.car.model} - {self.discount_percentage}% Off"

class PromoBanner(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=200)
    button_text = models.CharField(max_length=50, default="Learn More")
    button_link = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_date']

class ServiceBenefit(models.Model):
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title