from django.urls import path

from . import views

app_name = "ingredients"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("add/", views.AddIngredientView.as_view(), name="add_ingredient"),
    path("<int:pk>/", views.IngredientDetailsView.as_view(), name="details")
]