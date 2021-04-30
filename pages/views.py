import copy
import json
import random

from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from storesdisplay.models import Stores, User, Inventory, Products, ShoppingCart, PaymentInfo, Transactions


# Create your views here.
def home_view(request, *args, **kwargs):
    stores = Stores.objects.all()
    return render(request, "home.html", {"stores": stores})


def store_view(request, *args, **kwargs):
    if request.method == 'POST':
        # HANDLE "ADD TO CART"
        # form = json.loads(request.body)
        form = json.loads(request.body.decode('utf-8'))

        # GET USER INFORMATION (IN FUTURE INCLUDE THIS IN COOKIE?)
        form_user = form["user"]
        user = User.objects.get(user_name__iexact=form_user["user_name"],
                                user_password__iexact=form_user["user_password"])

        # GET PRODUCT INFORMATION
        product = Products.objects.get(product_id__iexact=form["product_id"])

        # ADD TO SHOPPING CART
        try:
            cart_entry = ShoppingCart.objects.get(user_id__iexact=user.user_id,
                                                  product_id__iexact=product.product_id)

            # SHOPPING CART ENTRY SHOULD EXIST BEYOND THIS POINT
            # INCREMENT QUANTITY AND SAVE ENTRY
            cart_entry.quantity += 1
            quantity = cart_entry.quantity
            cart_entry.save()
        except:
            # SHOPPING CART ENTRY DOES NOT EXIST
            # CREATE NEW SHOPPING CART ENTRY
            ShoppingCart.objects.create(
                user_id=user.user_id,
                product_id=product.product_id,
                quantity=1
            )
            quantity = 1

        form["success"] = {
            "user": user.user_id,
            "product": product.product_name,
            "quantity": quantity
        }

        return HttpResponse(json.dumps(form))
    else:
        store = Stores.objects.get(store_id__iexact=kwargs["store_id"])
        context = {
            "store_name": store.store_name,
            "store_address": store.store_address,
            "best_sellers": [],
            "containers": []
        }

        # GET PRODUCT INFORMATION
        inventory = Inventory.objects.filter(store_id__iexact=kwargs["store_id"])
        counter = 0
        container = []

        for item in inventory:
            counter += 1
            product = Products.objects.get(product_id__iexact=item.product_id)

            # TODO: PRODUCT IMAGE TABLE WAS NOT ADDED, ADD THIS JANKY FIX
            # COPY PRODUCT OBJECT AND ADD IMAGE NAME
            product_edited = copy.deepcopy(product)
            product_edited.image_path = "images/item_images/" + str(product.product_name).lower().replace(" ", "_") + ".png"

            container.append(product_edited)
            if counter % 4 == 0 and counter != 0:
                context["containers"].append(container)
                container = []

            # GET 5 PRODUCTS FOR "BEST SELLERS"
            if counter <= 5:
                context["best_sellers"].append(product_edited)

        # IF THERE ARE LEFTOVER PRODUCTS, ADD THEM
        if len(container) > 0:
            context["containers"].append(container)

        # DISPLAY PAGE
        return render(request, "store.html", context)


def signin_view(request, *args, **kwargs):
    if request.method == 'POST':
        # CHECK IF ACCOUNT IS VALID
        form = json.loads(request.body.decode('utf-8'))

        # CHECK USER NAME
        try:
            user = User.objects.get(user_name__iexact=form["username"])
            password = user.user_password
            if form["password"] != password:
                form["error"] = "Invalid Password"
                return HttpResponse(json.dumps(form))
        except:
            form["error"] = "Invalid Username"
            return HttpResponse(json.dumps(form))

        form["success"] = {
            "id": user.user_id,
            "user_name": user.user_name,
            "user_password": user.user_password,
            "user_first": user.user_first,
            "user_last": user.user_last
        }
        return HttpResponse(json.dumps(form))
    else:
        return render(request, "signin.html", {})


def signup_view(request, *args, **kwargs):
    if request.method == 'POST':
        # CHECK IF ACCOUNT IS VALID
        form = json.loads(request.body.decode('utf-8'))

        users = User.objects.all()
        user_id = "u" + str(len(users) + 1)
        permission = 1  # PERMISSION: 1 = basic user ; 2 = driver ; 3 = site administrator

        # TODO: MAYBE SOME CONFIRMATION THAT NO DUPLICATE USERNAME EXISTS?

        # UPLOAD NEW ACCOUNT DATA TO DATABASE
        User.objects.create(
            user_id=user_id,
            user_name=form["username"],
            user_password=form["password"],
            user_first=form["firstname"],
            user_last=form["lastname"],
            permission=permission,
            user_address=form["address"],
            user_email=form["email"],
            user_phone=form["phoneNumber"]
        )

        form["success"] = {
            "id": user_id,
            "user_name": form["username"],
            "user_password": form["password"],
            "user_first": form["firstname"],
            "user_last": form["lastname"]
        }
        return HttpResponse(json.dumps(form))
    else:
        return render(request, "signup.html", {})


def shopping_cart(request, *args, **kwargs):
    if request.method == 'POST':
        form = json.loads(request.body.decode('utf-8'))

        if "update" in form:
            # UPDATE USER'S SHOPPING CART WITH THE GIVEN QUANTITIES
            updated_cart = form["update"]
            # GET USER SHOPPING CART INFORMATION
            user_cart = ShoppingCart.objects.filter(user_id__iexact=form["user"]["id"])
            for cart_item in user_cart:
                product = Products.objects.get(product_id__iexact=cart_item.product_id)
                # UPDATE CART IF QUANTITY > 0, ELSE DELETE OBJECT FROM SHOPPING CART
                if updated_cart[product.product_name] > 0:
                    cart_item.quantity = updated_cart[product.product_name]
                    cart_item.save()
                else:
                    cart_item.delete()
            return HttpResponse("{}")
        else:
            # GET USER INFORMATION
            form = json.loads(request.body.decode('utf-8'))["user"]

            # GET USER SHOPPING CART INFORMATION
            user_cart = ShoppingCart.objects.filter(user_id__iexact=form["id"])

            cart = []
            for cart_item in user_cart:
                product_id = cart_item.product_id
                product = Products.objects.get(product_id__iexact=product_id)
                entry = {
                    "name": product.product_name,
                    "quantity": cart_item.quantity,
                    "base_price": '%.2f' % product.price,
                    "total_price": '%.2f' % (product.price * cart_item.quantity)
                }
                cart.append(entry)

            form["success"] = cart

            return HttpResponse(json.dumps(form))
    else:
        return render(request, "shopping_cart.html", {})


def checkout(request, *args, **kwargs):
    if request.method == "POST":
        form = json.loads(request.body.decode('utf-8'))
        if "checkout" in form:
            print("do checkout")
            print(form)
            # SAVE CREDIT CARD DETAILS
            try:
                payment = PaymentInfo.objects.get(user_id__iexact=form["user"]["id"])
                # DETAILS EXIST, UPDATE
                payment.card_number = form["checkout"]["payment"]["card_number"]
                payment.expiration = form["checkout"]["payment"]["expiry_date"]
                payment.card_ccv = form["checkout"]["payment"]["cvv"]
                payment.save()
            except ObjectDoesNotExist:
                print("no payment entry")
                # CREATE PAYMENT INFO ENTRY
                PaymentInfo.objects.create(
                    payment_id=("p" + str(len(PaymentInfo.objects.all()) + 1)),
                    user_id=form["user"]["id"],
                    card_company="",
                    card_number=form["checkout"]["payment"]["card_number"],
                    card_expiration=datetime.now(),
                    card_ccv=form["checkout"]["payment"]["cvv"]
                )
                print("created payment info")

            # CREATE NEW TRANSACTION ENTRY (order_id === rating now btw)
            Transactions.objects.create(
                transaction_id=("t" + str(len(Transactions.objects.all()) + 1)),
                user_id=form["user"]["id"],
                order_id=0,
                transaction_date=datetime.now(),
                transaction_price=float(form["checkout"]["order"]["price"])
            )

            # DELETE USER SHOPPING CART
            user_cart = ShoppingCart.objects.filter(user_id__iexact=form["user"]["id"])
            user_cart.delete()

            # CHECKOUT SHOULD BE COMPLETE
            return HttpResponse("{}")
        else:
            # GET USER INFORMATION
            form = form["user"]

            # GET USER SHOPPING CART INFORMATION
            user_cart = ShoppingCart.objects.filter(user_id__iexact=form["id"])

            cart = []
            for cart_item in user_cart:
                product_id = cart_item.product_id
                product = Products.objects.get(product_id__iexact=product_id)
                entry = {
                    "name": product.product_name,
                    "quantity": cart_item.quantity,
                    "base_price": '%.2f' % product.price,
                    "total_price": '%.2f' % (product.price * cart_item.quantity)
                }
                cart.append(entry)

            form["success"] = {}
            form["success"]["cart"] = cart

            # GET USER ADDRESS
            user = User.objects.get(user_id__iexact=form["id"])
            form["success"]["address"] = user.user_address

            # GET USER CREDIT CARD DETAILS
            form["success"]["payment"] = {
                "card_number": "",
                "expiry_date": "",
                "cvv": ""
            }
            try:
                payment = PaymentInfo.objects.get(user_id__iexact=user.user_id)
                form["success"]["payment"] = {
                    "card_number": payment.card_number,
                    "expiry_date": payment.card_expiration.strftime("%Y-%m-%d"),
                    "cvv": payment.card_ccv
                }
            except ObjectDoesNotExist:
                print("no payment set")

            return HttpResponse(json.dumps(form))
    else:
        return render(request, "checkout_details.html", {})


def contact_view(request, *args, **kwargs):
    return render(request, "contact.html", {})


def orders(request, *args, **kwargs):
    if request.method == "POST":
        form = json.loads(request.body.decode('utf-8'))
        if "rating" in form:
            print(form)
            print("do rating")
            transaction = Transactions.objects.get(transaction_id__iexact=form["rating"]["id"])
            # USING order_id AS A RATING VALUE
            transaction.order_id = form["rating"]["rating"]
            transaction.save()

            return HttpResponse("{}")
        else:
            print("get last order details")
            # GET LAST TRANSACTION BY USER
            transactions = Transactions.objects.filter(user_id__iexact=form["user"]["id"])
            last_transaction = transactions[len(transactions) - 1]
            print(last_transaction.transaction_id, last_transaction.transaction_price)

            # GET A RANDOM DRIVER
            drivers = User.objects.filter(permission__iexact=3)
            driver = random.choice(drivers)

            form["success"] = {
                "id": last_transaction.transaction_id,
                "date": last_transaction.transaction_date.strftime("%Y-%m-%d"),
                "price": last_transaction.transaction_price,
                "driver": {
                    "first": driver.user_first,
                    "last": driver.user_last
                }
            }
            return HttpResponse(json.dumps(form))
    else:
        return render(request, "users_order.html", {})