from django.contrib import admin
from .models import Comment, Post

# from .models import Recipe, Rating, RecipeComment

# Register your models here.


# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "publish", "status"]
    list_filter = ["status", "created", "publish", "author"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]
    date_hierarchy = "publish"
    ordering = ["status", "publish"]
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "post", "created", "active"]
    list_filter = ["active", "created", "updated"]
    search_fields = ["name", "email", "body"]


# @admin.register(Recipe)
# class RecipeAdmin(admin.ModelAdmin):
#     list_display = ["title", "slug", "author", "prep_time", "publish"]
#     list_filter = ["publish"]
#     search_fields = ["title", "body", "ingredients"]
#     prepopulated_fields = {"slug": ("title",)}
#     raw_id_fields = ["author"]
#     date_hierarchy = "publish"
#     ordering = ["publish"]

#     def get_average_rating(self, obj):
#         return obj.average_rating

#     get_average_rating.short_description = "Average Rating"


# @admin.register(Rating)
# class RatingAdmin(admin.ModelAdmin):
#     list_display = ["recipe", "user", "score"]
#     list_filter = ["score", "user"]
#     search_fields = ["recipe__title", "user__username"]


# @admin.register(RecipeComment)
# class RecipeCommentAdmin(admin.ModelAdmin):
#     list_display = ["name", "email", "recipe", "created", "active"]
#     list_filter = ["active", "created", "updated"]
#     search_fields = ["name", "email", "body"]
