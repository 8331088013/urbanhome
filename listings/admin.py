from django.contrib import admin
from .models import Property, PropertyImage, Contact, Favorite, PropertyReview, Message, Country, State, City, Town, Village
from django import forms

class PropertyAdminForm(forms.ModelForm):
    amenities = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Gym, Pool, Garden'}),
        help_text="Enter amenities separated by commas (e.g., Gym, Pool, Garden)"
    )

    def clean_amenities(self):
        data = self.cleaned_data['amenities']
        if data:
            return [item.strip() for item in data.split(',') if item.strip()]
        return []

    class Meta:
        model = Property
        fields = '__all__'

class PropertyAdmin(admin.ModelAdmin):
    form = PropertyAdminForm
    list_display = ['title', 'owner', 'property_type', 'price', 'city', 'bhk', 'is_active', 'is_featured', 'created_at']
    list_filter = ['property_type', 'furnished', 'is_active', 'is_featured', 'city', 'created_at']
    search_fields = ['title', 'description', 'city', 'area_name', 'owner__email']
    list_editable = ['is_active', 'is_featured']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('owner', 'title', 'description', 'property_type', 'price')
        }),
        ('Property Details', {
            'fields': ('bhk', 'area', 'furnished', 'bathrooms', 'balconies', 'parking')
        }),
        ('Location', {
            'fields': ('city', 'area_name', 'address', 'pincode', 'latitude', 'longitude')
        }),
        ('Additional Details', {
            'fields': ('amenities', 'virtual_tour_url', 'floor_number', 'total_floors', 'age_of_property')
        }),
        ('Media', {
            'fields': ('main_image',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured', 'created_at', 'updated_at')
        }),
    )

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'caption', 'image']
    list_filter = ['property__city']
    search_fields = ['property__title', 'caption']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'property', 'created_at']
    list_filter = ['created_at', 'property__city']
    search_fields = ['name', 'email', 'phone', 'property__title']
    readonly_fields = ['created_at']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'property', 'created_at']
    list_filter = ['created_at', 'property__city']
    search_fields = ['user__email', 'property__title']
    readonly_fields = ['created_at']

@admin.register(PropertyReview)
class PropertyReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'property', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'property__city']
    search_fields = ['user__email', 'property__title', 'comment']
    readonly_fields = ['created_at']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'subject', 'property', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at', 'property__city']
    search_fields = ['sender__email', 'receiver__email', 'subject', 'message', 'property__title']
    readonly_fields = ['created_at']
    list_editable = ['is_read']

admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Town)
admin.site.register(Village)

admin.site.register(Property, PropertyAdmin)
