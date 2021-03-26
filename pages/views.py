import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from storesdisplay.models import Stores, User, Inventory, Products


# Create your views here.
def home_view(request, *args, **kwargs):
    stores = Stores.objects.all()
    return render(request, "home.html", {"stores": stores})


def store_view(request, *args, **kwargs):
    store = Stores.objects.get(store_id__iexact=kwargs["store_id"])
    context = {
        "store_name": store.store_name,
        "store_address": store.store_address,
        "products": []
    }

    # GET RANDOM 5 PRODUCTS HERE
    inventory = Inventory.objects.filter(store_id__iexact=kwargs["store_id"])
    counter = 0
    for item in inventory:
        counter += 1
        product = Products.objects.get(product_id__iexact=item.product_id)
        context["products"].append(product.product_name)

        # STOP LOOPING AFTER 5 ITEMS
        if counter >= 5:
            break

    # DISPLAY PAGE
    return render(request, "store.html", context)


def signin_view(request, *args, **kwargs):
    # TODO
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
    # TODO
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


def contact_view(request, *args, **kwargs):
    return render(request, "contact.html", {})
