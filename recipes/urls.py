from django.urls import path

from . import views

app_name = "recipes"

urlpatterns = [
    path("", views.SeeAllRecipesView.as_view(), name="index"),
    path("add/", views.AddRecipeView.as_view(), name="add_recipe"),
    path("<int:pk>/", views.RecipeDetailsView.as_view(), name="details"),
    path("<int:pk>/edit/", views.EditRecipeView.as_view(), name="edit_recipe")
]