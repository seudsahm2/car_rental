from django.db import models
from django.utils.text import slugify
from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from django.contrib import admin
from django.utils.html import format_html


class CarCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    category = models.ForeignKey(CarCategory, on_delete=models.SET_NULL, null=True, blank=True)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    image_path = models.CharField(max_length=255, blank=True, null=True)  # Store Supabase file path
    description = models.TextField(blank=True)
    seats = models.PositiveIntegerField()
    insurance_included = models.BooleanField(default=True)
    usdt_accepted = models.BooleanField(default=True)
    whatsapp_deal = models.BooleanField(default=True)
    no_security_deposit = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.make} {self.model} {self.year}")
            self.slug = base_slug
            counter = 1
            while Car.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

class FAQCategory(models.Model):  # New model for FAQ categories
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class FAQ(models.Model):    
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.ForeignKey(FAQCategory, on_delete=models.SET_NULL, null=True, blank=True)  # Updated to use ForeignKey
    slug = models.SlugField(unique=True, blank=True)  # Added for SEO
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.question)
            counter = 1
            while FAQ.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.question
    
class ContentSection(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    page = models.CharField(max_length=100, default='luxury')  # e.g., 'luxury', 'sports'
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
class CustomerReview(models.Model):
    name = models.CharField(max_length=100)
    review = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            counter = 1
            while CustomerReview.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
class SiteInfo(models.Model):
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    hours = models.CharField(max_length=100, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "Site Information"

class AdUnit(models.Model):
    name = models.CharField(max_length=100)
    ad_slot = models.CharField(max_length=50, blank=True, help_text="Google AdSense ad slot ID")
    page = models.CharField(max_length=100, default='all', help_text="Page where ad appears, e.g., 'about', 'home', or 'all' for site-wide")
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            counter = 1
            while AdUnit.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
