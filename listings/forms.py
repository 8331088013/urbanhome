from django import forms
from .models import Property, PropertyImage, Contact, PropertyReview, Message, Country, State, City, Town, Village

class PropertyForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    state = forms.ModelChoiceField(queryset=State.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    town = forms.ModelChoiceField(queryset=Town.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    village = forms.ModelChoiceField(queryset=Village.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    latitude = forms.DecimalField(required=False, widget=forms.HiddenInput())
    longitude = forms.DecimalField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Property
        exclude = ['owner', 'created_at', 'updated_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter property title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter property description'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'bhk': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of bedrooms'}),
            'area': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Area in square feet'}),
            'furnished': forms.Select(attrs={'class': 'form-select'}),
            'area_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter area/locality'}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter pincode'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'balconies': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'parking': forms.Select(attrs={'class': 'form-select'}),
            'main_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'amenities': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comma separated amenities'}),
            'virtual_tour_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Virtual tour URL (optional)'}),
            'floor_number': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'total_floors': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'age_of_property': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Age in years'}),
        }

    def clean_amenities(self):
        amenities = self.cleaned_data.get('amenities')
        if amenities:
            # Convert comma-separated string to list
            amenities_list = [amenity.strip() for amenity in amenities.split(',') if amenity.strip()]
            return amenities_list
        return []

class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'caption']

class PropertySearchForm(forms.Form):
    PROPERTY_TYPES = [
        ('', 'All Types'),
        ('rent', 'For Rent'),
        ('sale', 'For Sale'),
    ]
    
    BHK_CHOICES = [
        ('', 'Any BHK'),
        ('1', '1 BHK'),
        ('2', '2 BHK'),
        ('3', '3 BHK'),
        ('4', '4 BHK'),
        ('5+', '5+ BHK'),
    ]
    
    FURNISHED_CHOICES = [
        ('', 'Any Furnished Status'),
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    
    SORT_CHOICES = [
        ('-created_at', 'Newest First'),
        ('price_low', 'Price: Low to High'),
        ('price_high', 'Price: High to Low'),
        ('rating', 'Highest Rated'),
    ]
    
    search = forms.CharField(max_length=200, required=False, 
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by city, area...'}))
    property_type = forms.ChoiceField(choices=PROPERTY_TYPES, required=False, 
                                    widget=forms.Select(attrs={'class': 'form-select'}))
    bhk = forms.ChoiceField(choices=BHK_CHOICES, required=False,
                          widget=forms.Select(attrs={'class': 'form-select'}))
    furnished = forms.ChoiceField(choices=FURNISHED_CHOICES, required=False,
                                widget=forms.Select(attrs={'class': 'form-select'}))
    min_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False,
                                 widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min Price'}))
    max_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False,
                                 widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max Price'}))
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False, initial='-created_at',
                              widget=forms.Select(attrs={'class': 'form-select'}))

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your phone number'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your message...'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = PropertyReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Share your experience...'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Message subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your message to the owner...'}),
        }

class PropertyAdminForm(forms.ModelForm):
    amenities = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Gym, Pool, Garden'}),
        help_text="Enter amenities separated by commas (e.g., Gym, Pool, Garden)"
    )

    def clean_amenities(self):
        data = self.cleaned_data['amenities']
        if data:
            # Convert comma-separated string to list
            return [item.strip() for item in data.split(',') if item.strip()]
        return []

    class Meta:
        model = Property
        fields = '__all__'