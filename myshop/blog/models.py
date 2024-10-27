from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models import Avg
from taggit.managers import TaggableManager


# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_posts",  # user.blog_posts
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    # publish = models.DateTimeField(db_default=Now()) # //Database DateTime Now
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )

    # The reverse() function will build the URL dynamically using the URL name defined in the URL patterns.

    tags = TaggableManager()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"


# class Recipe(Post):
#     ingredients = models.TextField()
#     prep_time = models.IntegerField(help_text="Preparation time in minutes")
#     cook_time = models.IntegerField(help_text="Cooking time in minutes")
#     # average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

#     @property
#     def average_rating(self):
#         return self.ratings.aggregate(average=Avg("score"))["average"] or 0.0

#     def __str__(self):
#         return f"{self.title} - {self.average_rating:.2f}"

#     def get_absolute_url(self):
#         return reverse(
#             "blog:recipe_detail",
#             args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
#         )


# class Rating(models.Model):
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ratings")
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     score = models.PositiveIntegerField(default=1)

#     class Meta:
#         unique_together = ("recipe", "user")


# class RecipeComment(models.Model):
#     recipe = models.ForeignKey(
#         Recipe, on_delete=models.CASCADE, related_name="recipe_comments"
#     )
#     name = models.CharField(max_length=80)
#     email = models.EmailField()
#     body = models.TextField()
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     active = models.BooleanField(default=True)

#     class Meta:
#         ordering = ["created"]
#         indexes = [
#             models.Index(fields=["created"]),
#         ]

#     def __str__(self):
#         return f"Comment by {self.name} on {self.recipe}"
