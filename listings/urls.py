from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.property_list, name='list'),
    path('property/<int:pk>/', views.property_detail, name='detail'),
    path('add/', views.add_property, name='add_property'),
    path('property/<int:pk>/edit/', views.edit_property, name='edit_property'),
    path('property/<int:pk>/delete/', views.delete_property, name='delete_property'),
    path('my-properties/', views.my_properties, name='my_properties'),
    path('favorites/', views.my_favorites, name='my_favorites'),
    path('property/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('messages/', views.messages_list, name='messages'),
    path('message/<int:pk>/', views.message_detail, name='message_detail'),
    path('ajax/get-states/', views.get_states, name='get_states'),
    path('ajax/get-cities/', views.get_cities, name='get_cities'),
    path('ajax/get-towns/', views.get_towns, name='get_towns'),
    path('ajax/get-villages/', views.get_villages, name='get_villages'),
]