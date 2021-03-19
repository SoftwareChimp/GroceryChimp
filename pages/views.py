from django.http import HttpResponse
from django.shortcuts import render
from storesdisplay.models import Stores


# Create your views here.
def home_view(request, *args, **kwargs):
    stores = Stores.objects.all()

    return render(request, "home.html", {"stores": stores})


def contact_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Contact Page</h1>")
    return render(request, "contact.html", {})
