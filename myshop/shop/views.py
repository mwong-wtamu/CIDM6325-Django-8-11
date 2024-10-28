from django.shortcuts import get_object_or_404, render
from .models import Category, Product
from cart.forms import CartAddProductForm
from .recommender import Recommender
from django.shortcuts import redirect
from django.urls import reverse


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(
        request,
        "shop/product/list.html",
        {"category": category, "categories": categories, "products": products},
    )


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(
        request,
        "shop/product/detail.html",
        {
            "product": product,
            "cart_product_form": cart_product_form,
            "recommended_products": recommended_products,
        },
    )


def payment_required(request):
    product_id = 5
    slug = "premium-recipes"

    product_url = reverse("shop:product_detail", args=[product_id, slug])
    print("Redirecting to:", product_url)
    return redirect(product_url)
