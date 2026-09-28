from django.urls import path
from . import views

app_name = 'user_settings' # Helps with namespacing

urlpatterns = [
    path('', views.settings_view, name='user_settings'),
    path('delete-account/', views.delete_account_view, name='delete_account'),
]