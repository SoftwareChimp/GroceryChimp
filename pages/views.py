from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from storesdisplay.models import Stores


# Create your views here.
def home_view(request, *args, **kwargs):
    stores = Stores.objects.all()
    return render(request, "home.html", {"stores": stores})


def store_view(request, *args, **kwargs):
    store = Stores.objects.get(store_id__iexact=kwargs["store_id"])
    context = {
        "store_name": store.store_name,
        "store_address": store.store_address,
        "products": ["Product1", "Product2", "Product3", "Product4", "Product5"]
    }

    # GET RANDOM 5 PRODUCTS HERE

    # DISPLAY PAGE
    return render(request, "store.html", context)


def register_account_view(request, *args, **kwargs):
    # TODO
    if request.method == 'POST':
        return HttpResponse("POST request get")
    else:
        return HttpResponseRedirect('/')  # RETURN TO HOME PAGE
        # return HttpResponse("no post request?")


def contact_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Contact Page</h1>")
    return render(request, "contact.html", {})
