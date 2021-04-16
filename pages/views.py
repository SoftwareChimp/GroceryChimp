import copy
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from storesdisplay.models import Stores, User, Inventory, Products, ShoppingCart


# Create your views here.
def home_view(request, *args, **kwargs):
    stores = Stores.objects.all()
    return render(request, "home.html", {"stores": stores})


def store_view(request, *args, **kwargs):
    if request.method == 'POST':
        # HANDLE "ADD TO CART"
        # form = json.loads(request.body)
        form = json.loads(request.body.decode('utf-8'))

        # TODO: USERS STILL USE FIRST_NAME LAST_NAME, REPLACE THIS IN FUTURE
        # GET USER INFORMATION (IN FUTURE INCLUDE THIS IN COOKIE?)
        name = str(form["user"]).split()
        user = User.objects.get(user_first__iexact=name[0], user_last__iexact=name[1])

        # GET PRODUCT INFORMATION
        product = Products.objects.get(product_id__iexact=form["product_id"])

        # ADD TO SHOPPING CART
        try:
            # TODO: THE SHOPPING CART MODEL (AND A GOOD NUMBER OF OTHERS) USE INTEGERS FOR THEIR IDS WHEN ...
            # TODO: ... THE USER AND PRODUCTS MODEL USE STRINGS. FIX THIS ISSUE?
            cart_entry = ShoppingCart.objects.get(user_id__iexact=int(user.user_id[1:]),
                                                  product_id__iexact=int(product.product_id[1:]))

            # SHOPPING CART ENTRY SHOULD EXIST BEYOND THIS POINT
            # INCREMENT QUANTITY AND SAVE ENTRY
            cart_entry.quantity += 1
            quantity = cart_entry.quantity
            cart_entry.save()
        except:
            # SHOPPING CART ENTRY DOES NOT EXIST
            # CREATE NEW SHOPPING CART ENTRY
            ShoppingCart.objects.create(
                user_id=int(user.user_id[1:]),
                product_id=int(product.product_id[1:]),
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
            # TODO: CURRENTLY user_name DOES NOT EXIST, USE user_first INSTEAD
            # TODO: SAME WITH user_password, USE user_last INSTEAD
            user = User.objects.get(user_first__iexact=form["username"])
            password = user.user_last
            if form["password"] != password:
                form["error"] = "Invalid Password"
                return HttpResponse(json.dumps(form))
        except:
            form["error"] = "Invalid Username"
            return HttpResponse(json.dumps(form))

        form["success"] = form["username"] + " " + form["password"]
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
        print(len(users))

        form["success"] = form["username"] + " " + form["password"]
        return HttpResponse(json.dumps(form))
    else:
        return render(request, "signup.html", {})


def shopping_cart(request, *args, **kwargs):
    if request.method == 'POST':
        form = json.loads(request.body.decode('utf-8'))

        # TODO: USERS STILL USE FIRST_NAME LAST_NAME, REPLACE THIS IN FUTURE
        # GET USER INFORMATION (IN FUTURE INCLUDE THIS IN COOKIE?)
        name = str(form["user"]).split()
        user = User.objects.get(user_first__iexact=name[0], user_last__iexact=name[1])

        # GET USER SHOPPING CART INFORMATION
        user_id = int(user.user_id[1:])
        user_cart = ShoppingCart.objects.filter(user_id__iexact=user_id)

        cart = []
        for cart_item in user_cart:
            product_id = "p" + str(cart_item.product_id)
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


def contact_view(request, *args, **kwargs):
    return render(request, "contact.html", {})
