from django.contrib import admin
from .models import Image
from recipes.models import Recipe


# Inline to show recipes associated with an image
class RecipeInline(admin.TabularInline):
    model = Recipe.images.through  # This links the intermediary table
    extra = 1  # Allows you to add additional relationships in the admin interface


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "image", "created"]
    list_filter = ["created"]
    inlines = [RecipeInline]  # Add the inline here
