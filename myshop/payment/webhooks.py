import stripe
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order, PaidUser
from .tasks import payment_completed
from shop.models import Product
from shop.recommender import Recommender


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    if event.type == "checkout.session.completed":
        session = event.data.object
        if session.mode == "payment" and session.payment_status == "paid":
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            # mark order as paid
            order.paid = True
            # store Stripe payment ID
            order.stripe_id = session.payment_intent
            order.save()

            # Retrieve product IDs for items in the order
            product_ids = order.items.values_list("product_id", flat=True)
            # print("Product IDs in order:", product_ids)  # Debugging statement

            # Define your target product IDs that qualify for premium access
            target_product_ids = {5}  # Cookbook
            # print("Target Product IDs for premium access:", target_product_ids)

            # Check if any product in the order matches a target product ID
            if any(product_id in target_product_ids for product_id in product_ids):
                # If criteria are met, update or create a PaidUser record
                # print("order.user")
                paid_user, created = PaidUser.objects.get_or_create(user=order.user)
                paid_user.is_paid = True
                paid_user.payment_date = timezone.now()
                paid_user.save()
                # print("Premium access granted.")
            # else:
            # print(
            #    "No qualifying product for premium access."
            # )  # Debugging statement

            # save items bought for product recommendations
            product_ids = order.items.values_list("product_id")
            products = Product.objects.filter(id__in=product_ids)
            r = Recommender()
            r.products_bought(products)
            # launch asynchronous task
            payment_completed.delay(order.id)
    return HttpResponse(status=200)
