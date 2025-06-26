from django.db import models

class SiteConfiguration(models.Model):
    google_adsense_client_id = models.CharField(max_length=100, blank=True)
    google_maps_api_key = models.CharField(max_length=100, blank=True)
    whatsapp_default_message = models.CharField(max_length=200, default="Hi, I'm interested in renting a car.")

    def __str__(self):
        return "Site Configuration"

    class Meta:
        verbose_name_plural = "Site Configuration"

class SocialMediaLink(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
    ]
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    icon_class = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.get_platform_display()}"

    class Meta:
        ordering = ['order']

class PageMeta(models.Model):
    PAGE_CHOICES = [
        ('home', 'Home'),
        ('about', 'About Us'),
        ('contact', 'Contact'),
        ('blog', 'Blog'),
        ('faq', 'FAQ'),
        ('dubai_marina', 'Dubai Marina'),
        ('airport', 'Airport Rentals'),
        ('monthly', 'Monthly Rentals'),
    ]
    page = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    keywords = models.TextField(blank=True)
    canonical_url = models.URLField(blank=True)

    def __str__(self):
        return f"SEO Meta for {self.get_page_display()}"

    class Meta:
        verbose_name = "Page Meta"
        verbose_name_plural = "Page Meta"

class Language(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Translation(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    value = models.TextField()

    def __str__(self):
        return f"{self.key} ({self.language.code})"

    class Meta:
        unique_together = ('language', 'key')