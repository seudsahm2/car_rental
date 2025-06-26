from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class BookingRequest(models.Model):
    # Use GenericForeignKey to avoid direct dependency on `fleet.Car`
    car_content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    car_object_id = models.PositiveIntegerField(null=True, blank=True)
    car = GenericForeignKey('car_content_type', 'car_object_id')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    pickup_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    message = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending'
    )

    def __str__(self):
        return f"Booking #{self.id} by {self.name}"

    class Meta:
        ordering = ['-submitted_at']

class ContactInquiry(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Inquiry from {self.name} ({self.phone})"

    class Meta:
        verbose_name_plural = "Contact Inquiries"