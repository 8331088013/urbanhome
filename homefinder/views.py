from django.shortcuts import render, redirect
from listings.models import Property
from listings.forms import PropertySearchForm
from .forms import ContactForm

def home(request):
    featured_listings = Property.objects.filter(is_active=True)[:6]
    search_form = PropertySearchForm()
    
    # Statistics
    total_properties = Property.objects.filter(is_active=True).count()
    properties_for_rent = Property.objects.filter(
        is_active=True, property_type='rent'
    ).count()
    properties_for_sale = Property.objects.filter(
        is_active=True, property_type='sale'
    ).count()
    
    context = {
        'featured_listings': featured_listings,
        'search_form': search_form,
        'total_properties': total_properties,
        'properties_for_rent': properties_for_rent,
        'properties_for_sale': properties_for_sale,
    }
    
    return render(request, 'homefinder/home.html', context)

def about(request):
    return render(request, 'homefinder/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'homefinder/contact.html', {'form': ContactForm(), 'success': True})
    else:
        form = ContactForm()
    return render(request, 'homefinder/contact.html', {'form': form})

# Create your views here.
