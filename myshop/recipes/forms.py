from django import forms

# from .models import Comment
from .models import Recipe, Rating, RecipeComment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "body", "ingredients", "prep_time", "cook_time"]


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["score"]


class RecipeCommentForm(forms.ModelForm):
    class Meta:
        model = RecipeComment
        fields = ["name", "email", "body"]
