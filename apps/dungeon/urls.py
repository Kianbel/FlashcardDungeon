from django.urls import path
from . import views

app_name = "dungeon"

urlpatterns = [
    path("forge/", views.forge_dungeon_view, name="forge_dungeon"),
    path("<int:deck_id>/", views.dungeon_detail_view, name="dungeon_detail"),
    path("<int:deck_id>/start/", views.start_run_view, name="start_run"),
    path("session/<int:session_id>/", views.review_run_view, name="review_run"),
    path("session/<int:session_id>/results/", views.run_results_view, name="run_results"),
]