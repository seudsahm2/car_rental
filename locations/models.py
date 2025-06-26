from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify

class Location(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    google_maps_embed_url = models.CharField(max_length=500, blank=True)
    order = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            counter = 1
            while Location.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']

class LocationSpecificDeal(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    # Generic relation to avoid direct dependency on `fleet.Car`
    featured_cars_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    featured_cars_object_ids = models.JSONField(default=list)  # Stores IDs of related cars
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.location.name}-{self.title}")
            counter = 1
            while LocationSpecificDeal.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.location.name})"

class PricingTier(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (x{self.multiplier})"