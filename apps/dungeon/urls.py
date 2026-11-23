from django.urls import path
from . import views

app_name = "dungeon"

urlpatterns = [
    path("forge/", views.forge_dungeon_view, name="forge_dungeon"),
    path("history/", views.run_history_view, name="run_history"),
    path("cursed/", views.cursed_foes_view, name="cursed_foes"),
    path("<int:deck_id>/", views.dungeon_detail_view, name="dungeon_detail"),
    path("<int:deck_id>/edit/", views.edit_deck_view, name="edit_deck"),
    path("<int:deck_id>/delete/", views.delete_deck_view, name="delete_deck"),
    path("<int:deck_id>/start/", views.start_run_view, name="start_run"),
    path("card/<int:card_id>/edit/", views.edit_card_view, name="edit_card"),
    path("card/<int:card_id>/delete/", views.delete_card_view, name="delete_card"),
    path("session/<int:session_id>/", views.review_run_view, name="review_run"),
    path("session/<int:session_id>/results/", views.run_results_view, name="run_results"),
]