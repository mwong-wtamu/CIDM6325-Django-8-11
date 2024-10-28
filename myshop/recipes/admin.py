from django.contrib import admin

# from .models import Comment, Post

from .models import Recipe, Rating, RecipeComment


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "is_premium",
        "slug",
        "author",
        "prep_time",
        "publish",
    ]
    list_filter = ["publish"]
    search_fields = ["title", "body", "ingredients"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]
    date_hierarchy = "publish"
    ordering = ["publish"]
    filter_horizontal = (
        "images",
    )  # Enables a horizontal filter for images in the admin

    def get_average_rating(self, obj):
        return obj.average_rating

    get_average_rating.short_description = "Average Rating"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ["recipe", "user", "score"]
    list_filter = ["score", "user"]
    search_fields = ["recipe__title", "user__username"]


@admin.register(RecipeComment)
class RecipeCommentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "recipe", "created", "active"]
    list_filter = ["active", "created", "updated"]
    search_fields = ["name", "email", "body"]
