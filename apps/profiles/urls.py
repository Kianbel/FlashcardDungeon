from django.urls import path
from . import views

app_name = 'profiles' # Helps with namespacing

urlpatterns = [
    path('', views.profile_view, name='profiles'),
    path('equip-title/', views.equip_title_view, name='equip_title'),
]