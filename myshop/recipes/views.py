from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import Http404
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import Avg, Count
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    TrigramSimilarity,
)
from taggit.models import Tag

# from .models import Post
from .models import Recipe, Rating
from orders.models import PaidUser

# from .forms import CommentForm, EmailPostForm, SearchForm
from .forms import RecipeCommentForm, RatingForm, EmailPostForm
from actions.utils import create_action

import redis
from django.conf import settings

# connect to redis
r = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


def recipe_list(request, tag_slug=None):

    # if (
    #     request.user.is_authenticated
    #     and hasattr(request.user, "paid_user")
    #     and request.user.paid_user.is_paid
    # ):
    # Show all recipes to paid users
    recipes_list = Recipe.published.all()
    # else:
    #     # Show only non-premium recipes to non-paid users
    #     recipes_list = Recipe.published.filter(is_premium=False)

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        recipes_list = recipes_list.filter(tags__in=[tag])

    paginator = Paginator(recipes_list, 3)
    page_number = request.GET.get("page", 1)
    try:
        recipes = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer get the first page
        recipes = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range get last page of results
        recipes = paginator.page(paginator.num_pages)
    return render(
        request, "recipes/recipe/recipe_list.html", {"recipes": recipes, "tag": tag}
    )


def recipe_detail(request, year, month, day, recipe):
    recipe = get_object_or_404(
        Recipe,
        status=Recipe.Status.PUBLISHED,
        slug=recipe,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    if recipe.is_premium and not (
        request.user.is_authenticated
        and hasattr(request.user, "paid_user")
        and request.user.paid_user.is_paid
    ):
        return redirect("shop:payment_required")

    # List of active comments for this recipe
    comments = recipe.recipe_comments.filter(active=True)

    form = RecipeCommentForm()  # Create an empty form to render on the page
    # List of similar recipes
    recipe_tags_ids = recipe.tags.values_list("id", flat=True)
    similar_recipes = Recipe.published.filter(tags__in=recipe_tags_ids).exclude(
        id=recipe.id
    )
    similar_recipes = similar_recipes.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:4]

    # Form for users to comment on recipe
    rating_form = RatingForm()
    average_rating = recipe.average_rating

    # increment total image views by 1
    # for redis
    total_views = r.incr(f"recipe:{recipe.id}:views")

    return render(
        request,
        "recipes/recipe/recipe_detail.html",
        {
            "recipe": recipe,
            "comments": comments,
            "form": form,
            "rating_form": rating_form,
            "average_rating": average_rating,
            "similar_recipes": similar_recipes,
            "total_views": total_views,
        },
    )


@require_POST
def rate_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, status=Recipe.Status.PUBLISHED)

    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, created = Rating.objects.update_or_create(
                recipe=recipe,
                user=request.user,
                defaults={"score": form.cleaned_data["score"]},
            )
            return render(
                request,
                "recipes/recipe/rate_recipe.html",
                {"rating": rating, "recipe": recipe},
            )
    else:
        form = RatingForm()

    return render(
        request,
        "recipes/recipe/rate_recipe.html",
        {"rating_form": form, "recipe": recipe},
    )


@require_POST
def recipe_comment(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, status=Recipe.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = RecipeCommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the recipe to the comment
        comment.recipe = recipe
        # Save the comment to the database
        comment.save()

    return render(
        request,
        "recipes/recipe/comment.html",
        {"recipe": recipe, "form": form, "comment": comment},
    )


def recipe_share(request, recipe_id):
    # Retrieve post by id
    recipe = get_object_or_404(Recipe, id=recipe_id, status=Recipe.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(recipe.get_absolute_url())
            subject = (
                f"{cd['name']} ({cd['email']}) " f"recommends you read {recipe.title}"
            )
            message = (
                f"Read {recipe.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd["to"]],
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request,
        "recipes/recipe/recipe_share.html",
        {"recipe": recipe, "form": form, "sent": sent},
    )


@login_required
@require_POST
def recipe_like(request):
    recipe_id = request.POST.get("id")
    action = request.POST.get("action")
    if recipe_id and action:
        try:
            recipe = Recipe.objects.get(id=recipe_id)
            if action == "like":
                recipe.users_like.add(request.user)
                create_action(request.user, "likes", recipe)
            else:
                recipe.users_like.remove(request.user)
            return JsonResponse({"status": "ok"})
        except Recipe.DoesNotExist:
            pass
    return JsonResponse({"status": "error"})
