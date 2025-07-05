from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Property, PropertyImage, Contact, Favorite, PropertyReview, Message, State, City, Town, Village
from .forms import PropertyForm, PropertyImageForm, PropertySearchForm, ContactForm, ReviewForm, MessageForm

def property_list(request):
    properties = Property.objects.filter(is_active=True).annotate(
        avg_rating=Avg('reviews__rating'),
        reviews_count=Count('reviews'),
        favorites_count=Count('favorites')
    )
    search_form = PropertySearchForm(request.GET)
    
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search')
        property_type = search_form.cleaned_data.get('property_type')
        bhk = search_form.cleaned_data.get('bhk')
        furnished = search_form.cleaned_data.get('furnished')
        min_price = search_form.cleaned_data.get('min_price')
        max_price = search_form.cleaned_data.get('max_price')
        
        if search_query:
            properties = properties.filter(
                Q(title__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(area_name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        if property_type:
            properties = properties.filter(property_type=property_type)
        
        if bhk:
            properties = properties.filter(bhk=bhk)
        
        if furnished:
            properties = properties.filter(furnished=furnished)
        
        if min_price:
            properties = properties.filter(price__gte=min_price)
        
        if max_price:
            properties = properties.filter(price__lte=max_price)
    
    # Sort options
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by == 'price_low':
        properties = properties.order_by('price')
    elif sort_by == 'price_high':
        properties = properties.order_by('-price')
    elif sort_by == 'rating':
        properties = properties.order_by('-avg_rating')
    else:
        properties = properties.order_by('-created_at')
    
    paginator = Paginator(properties, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get user favorites for highlighting
    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(user=request.user).values_list('property_id', flat=True)
    
    return render(request, 'listings/property_list.html', {
        'page_obj': page_obj,
        'search_form': search_form,
        'properties_count': properties.count(),
        'user_favorites': user_favorites,
    })

def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk, is_active=True)
    related_properties = Property.objects.filter(
        city=property.city, is_active=True
    ).exclude(pk=pk)[:4]
    
    contact_form = ContactForm()
    review_form = ReviewForm()
    message_form = MessageForm()
    
    # Check if user has favorited this property
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, property=property).exists()
    
    # Get reviews
    reviews = property.reviews.all().order_by('-created_at')
    
    if request.method == 'POST':
        if 'contact' in request.POST:
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                contact = contact_form.save(commit=False)
                contact.property = property
                contact.save()
                messages.success(request, 'Your message has been sent successfully!')
                return redirect('listings:detail', pk=pk)
        elif 'review' in request.POST and request.user.is_authenticated:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.property = property
                review.save()
                messages.success(request, 'Review submitted successfully!')
                return redirect('listings:detail', pk=pk)
        elif 'message' in request.POST and request.user.is_authenticated:
            message_form = MessageForm(request.POST)
            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.sender = request.user
                message.receiver = property.owner
                message.property = property
                message.save()
                messages.success(request, 'Message sent to owner!')
                return redirect('listings:detail', pk=pk)
    
    return render(request, 'listings/property_detail.html', {
        'property': property,
        'related_properties': related_properties,
        'contact_form': contact_form,
        'review_form': review_form,
        'message_form': message_form,
        'is_favorited': is_favorited,
        'reviews': reviews,
    })

@login_required
@require_POST
def toggle_favorite(request, pk):
    property = get_object_or_404(Property, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, property=property)
    
    if not created:
        favorite.delete()
        return JsonResponse({'status': 'removed', 'message': 'Removed from favorites'})
    
    return JsonResponse({'status': 'added', 'message': 'Added to favorites'})

@login_required
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('property')
    return render(request, 'listings/my_favorites.html', {'favorites': favorites})

@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.is_active = True  # Explicitly set as active
            property.save()
            messages.success(request, 'Property added successfully!')
            return redirect('listings:detail', pk=property.pk)
    else:
        form = PropertyForm()
    
    return render(request, 'listings/add_property.html', {'form': form})

@login_required
def edit_property(request, pk):
    property = get_object_or_404(Property, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            property = form.save(commit=False)
            property.is_active = True  # Ensure it stays active after editing
            property.save()
            messages.success(request, 'Property updated successfully!')
            return redirect('listings:detail', pk=property.pk)
    else:
        form = PropertyForm(instance=property)
    
    return render(request, 'listings/edit_property.html', {
        'form': form,
        'property': property,
    })

@login_required
def delete_property(request, pk):
    property = get_object_or_404(Property, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        property.delete()
        messages.success(request, 'Property deleted successfully!')
        return redirect('users:dashboard')
    
    return render(request, 'listings/delete_property.html', {'property': property})

@login_required
def my_properties(request):
    properties = Property.objects.filter(owner=request.user)
    return render(request, 'listings/my_properties.html', {'properties': properties})

@login_required
def messages_list(request):
    received_messages = Message.objects.filter(receiver=request.user).select_related('sender', 'property')
    sent_messages = Message.objects.filter(sender=request.user).select_related('receiver', 'property')
    
    return render(request, 'listings/messages.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
    })

@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)
    
    # Mark as read if receiver is viewing
    if message.receiver == request.user and not message.is_read:
        message.is_read = True
        message.save()
    
    return render(request, 'listings/message_detail.html', {'message': message})

def get_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).values('id', 'name')
    return JsonResponse(list(states), safe=False)

def get_cities(request):
    state_id = request.GET.get('state_id')
    cities = City.objects.filter(state_id=state_id).values('id', 'name')
    return JsonResponse(list(cities), safe=False)

def get_towns(request):
    city_id = request.GET.get('city_id')
    towns = Town.objects.filter(city_id=city_id).values('id', 'name')
    return JsonResponse(list(towns), safe=False)

def get_villages(request):
    town_id = request.GET.get('town_id')
    villages = Village.objects.filter(town_id=town_id).values('id', 'name')
    return JsonResponse(list(villages), safe=False)

# Create your views here.
