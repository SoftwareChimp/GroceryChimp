from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def home_view(request, *args, **kwargs):
    # ADD DATABASE READING CODE HERE
    context = {
        "stores": [
            {"name": "Global Fresh Market", "address": "784 Gulf St., Port Charlotte, FL 33952"},
            {"name": "Budget Foods", "address": "2 Creekside St., Flemington, NJ 08822"},
            {"name": "Dollar Pantry", "address": "8182 Westminster Street, Garden City, NY 11530"},
            {"name": "Food Festive", "address": "9709 East Lakeview Street, Coventry, RI 02816"},
            {"name": "Global Fresh Market", "address": "784 Gulf St., Port Charlotte, FL 33952"},
            {"name": "Budget Foods", "address": "2 Creekside St., Flemington, NJ 08822"},
            {"name": "Dollar Pantry", "address": "8182 Westminster Street, Garden City, NY 11530"},
            {"name": "Food Festive", "address": "9709 East Lakeview Street, Coventry, RI 02816"},
            {"name": "Global Fresh Market", "address": "784 Gulf St., Port Charlotte, FL 33952"},
            {"name": "Budget Foods", "address": "2 Creekside St., Flemington, NJ 08822"},
            {"name": "Dollar Pantry", "address": "8182 Westminster Street, Garden City, NY 11530"},
            {"name": "Food Festive", "address": "9709 East Lakeview Street, Coventry, RI 02816"},
            {"name": "Global Fresh Market", "address": "784 Gulf St., Port Charlotte, FL 33952"},
            {"name": "Budget Foods", "address": "2 Creekside St., Flemington, NJ 08822"},
            {"name": "Dollar Pantry", "address": "8182 Westminster Street, Garden City, NY 11530"},
            {"name": "Food Festive", "address": "9709 East Lakeview Street, Coventry, RI 02816"},
            {"name": "Global Fresh Market", "address": "784 Gulf St., Port Charlotte, FL 33952"},
            {"name": "Budget Foods", "address": "2 Creekside St., Flemington, NJ 08822"},
            {"name": "Dollar Pantry", "address": "8182 Westminster Street, Garden City, NY 11530"},
            {"name": "Food Festive", "address": "9709 East Lakeview Street, Coventry, RI 02816"}
        ]
    }
    # END DATABASE READING CODE
    return render(request, "home.html", context)


def contact_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Contact Page</h1>")
    return render(request, "contact.html", {})
