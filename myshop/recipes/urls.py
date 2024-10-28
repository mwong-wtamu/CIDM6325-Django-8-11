from django.urls import path
from . import views

app_name = "recipes"
urlpatterns = [
    # post views
    path("", views.recipe_list, name="recipe_list"),
    # path("", views.PostListView.as_view(), name="post_list"),
    path("tag/<slug:tag_slug>/", views.recipe_list, name="recipe_list_by_tag"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:recipe>/",
        views.recipe_detail,
        name="recipe_detail",
    ),
    path("<int:recipe_id>/rate/", views.rate_recipe, name="rate_recipe"),
    path("<int:recipe_id>/share/", views.recipe_share, name="recipe_share"),
    path("<int:recipe_id>/comment/", views.recipe_comment, name="recipe_comment"),
    path("like/", views.recipe_like, name="recipe_like"),
]
