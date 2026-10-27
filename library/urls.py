from django.urls import path

from . import views

app_name = "library"

urlpatterns = [
    path("", views.game_list, name="game_list"),
    path("games/add/", views.game_create, name="game_create"),
    path("games/<int:pk>/", views.game_detail, name="game_detail"),
    path("games/<int:pk>/edit/", views.game_update, name="game_update"),
    path("games/<int:pk>/delete/", views.game_delete, name="game_delete"),
    path("genres/", views.genre_list, name="genre_list"),
    path("genres/add/", views.genre_create, name="genre_create"),
    path("genres/<int:pk>/delete/", views.genre_delete, name="genre_delete"),
    path("platforms/", views.platform_list, name="platform_list"),
    path("platforms/add/", views.platform_create, name="platform_create"),
    path(
        "platforms/<int:pk>/delete/",
        views.platform_delete,
        name="platform_delete",
    ),
]
