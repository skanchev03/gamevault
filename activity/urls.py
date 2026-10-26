from django.urls import path

from . import views

app_name = "activity"

urlpatterns = [
    path("reviews/", views.review_list, name="review_list"),
    path("reviews/add/", views.review_create, name="review_create"),
    path("reviews/<int:pk>/", views.review_detail, name="review_detail"),
    path("reviews/<int:pk>/edit/", views.review_update, name="review_update"),
    path("reviews/<int:pk>/delete/", views.review_delete, name="review_delete"),
    path("sessions/", views.session_list, name="session_list"),
    path("sessions/add/", views.session_create, name="session_create"),
    path("sessions/<int:pk>/edit/", views.session_update, name="session_update"),
    path("sessions/<int:pk>/delete/", views.session_delete, name="session_delete"),
]
