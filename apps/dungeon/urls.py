from django.urls import path
from . import views

app_name = "dungeon"

urlpatterns = [
    path("forge/", views.forge_dungeon_view, name="forge_dungeon"),
    path("<int:deck_id>/", views.dungeon_detail_view, name="dungeon_detail"),
]