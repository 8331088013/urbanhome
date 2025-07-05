from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states')
    
    class Meta:
        unique_together = ('name', 'country')
    
    def __str__(self):
        return f"{self.name}, {self.country.name}"

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')
    
    class Meta:
        unique_together = ('name', 'state')
    
    def __str__(self):
        return f"{self.name}, {self.state.name}"

class Town(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='towns')
    
    class Meta:
        unique_together = ('name', 'city')
    
    def __str__(self):
        return f"{self.name}, {self.city.name}"

class Village(models.Model):
    name = models.CharField(max_length=100)
    town = models.ForeignKey(Town, on_delete=models.CASCADE, related_name='villages')
    
    class Meta:
        unique_together = ('name', 'town')
    
    def __str__(self):
        return f"{self.name}, {self.town.name}"

class Property(models.Model):
    PROPERTY_TYPES = [
        ('rent', 'For Rent'),
        ('sale', 'For Sale'),
    ]
    
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    
    BHK_CHOICES = [
        ('1', '1 BHK'),
        ('2', '2 BHK'),
        ('3', '3 BHK'),
        ('4', '4 BHK'),
        ('5+', '5+ BHK'),
    ]
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bhk = models.CharField(max_length=3, choices=BHK_CHOICES)
    area = models.IntegerField(help_text="Area in square feet")
    furnished = models.CharField(max_length=20, choices=FURNISHED_CHOICES)
    
    # Location
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    town = models.ForeignKey(Town, on_delete=models.SET_NULL, null=True, blank=True)
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True, blank=True)
    area_name = models.CharField(max_length=100)
    address = models.TextField()
    pincode = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Property details
    bathrooms = models.IntegerField(default=1)
    balconies = models.IntegerField(default=0)
    parking = models.BooleanField(default=False)
    
    # Additional amenities
    amenities = models.JSONField(default=list, blank=True)  # ['Gym', 'Pool', 'Garden']
    virtual_tour_url = models.URLField(blank=True)
    floor_number = models.IntegerField(null=True, blank=True)
    total_floors = models.IntegerField(null=True, blank=True)
    age_of_property = models.IntegerField(help_text="Age in years", null=True, blank=True)
    
    # Images
    main_image = models.ImageField(upload_to='property_images/', blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Properties'
    
    def __str__(self):
        return f"{self.title} - {self.city}"
    
    def get_absolute_url(self):
        return reverse('listings:property_detail', kwargs={'pk': self.pk})
    
    def get_favorites_count(self):
        return self.favorites.count()
    
    def get_average_rating(self):
        ratings = self.reviews.values_list('rating', flat=True)
        if ratings:
            return sum(ratings) / len(ratings)
        return 0

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'property']
    
    def __str__(self):
        return f"{self.user.email} - {self.property.title}"

class PropertyReview(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'property']
    
    def __str__(self):
        return f"{self.user.email} - {self.property.title} - {self.rating} stars"

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    caption = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"Image for {self.property.title}"

class Contact(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Contact for {self.property.title} by {self.name}"

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sender.email} to {self.receiver.email}: {self.subject}"

# Sample fixture for Property (save as listings/fixtures/sample_properties.json):
# [
#   {
#     "model": "listings.property",
#     "pk": 1,
#     "fields": {
#       "owner": 1,
#       "title": "Modern 2BHK Apartment in Bangalore",
#       "description": "Spacious, well-lit, close to metro.",
#       "property_type": "rent",
#       "price": "25000.00",
#       "bhk": "2",
#       "area": 1200,
#       "furnished": "furnished",
#       "city": "Bangalore",
#       "area_name": "Indiranagar",
#       "address": "123, 4th Main, Indiranagar",
#       "pincode": "560038",
#       "bathrooms": 2,
#       "balconies": 1,
#       "parking": true,
#       "main_image": "property_images/sample1.jpg",
#       "is_active": true
#     }
#   }
# ]
