from django.urls import path

from . import views

app_name = "recipes"

urlpatterns = [
    path("", views.SeeAllRecipesView.as_view(), name="index"),
    path("add/", views.AddRecipeView.as_view(), name="add_recipe")
]