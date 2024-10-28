from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    # post views
    path("", views.post_list, name="post_list"),
    # path("", views.PostListView.as_view(), name="post_list"),
    path("tag/<slug:tag_slug>/", views.post_list, name="post_list_by_tag"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.post_detail,
        name="post_detail",
    ),
    path("<int:post_id>/share/", views.post_share, name="post_share"),
    path("<int:post_id>/comment/", views.post_comment, name="post_comment"),
    path("search/", views.post_search, name="post_search"),
    # path("recipes/", views.recipe_list, name="recipe_list"),
    # path("recipes/tag/<slug:tag_slug>/", views.recipe_list, name="recipe_list_by_tag"),
    # path("recipes/<int:post_id>/", views.recipe_detail, name="recipe_detail"),
    # path(
    #     "recipes/<int:year>/<int:month>/<int:day>/<slug:recipe>/",
    #     views.recipe_detail,
    #     name="recipe_detail",
    # ),
    # path("recipes/<int:recipe_id>/rate/", views.rate_recipe, name="rate_recipe"),
    # path("recipes/<int:recipe_id>/share/", views.recipe_comment, name="recipe_comment"),
    # path(
    #     "recipes/<int:recipe_id>/comment/", views.recipe_comment, name="recipe_comment"),
]
