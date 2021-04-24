"""GroceryChimp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# my stuff
from pages.views import home_view, store_view, signin_view, signup_view, shopping_cart, checkout, contact_view

urlpatterns = [
    path('', home_view, name='home'),
    path('stores/<str:store_id>', store_view),
    path('signin/', signin_view),
    path('signup/', signup_view),
    path('shopping_cart/', shopping_cart),
    path('checkout/', checkout),
    path('contact/', contact_view,),
    path('admin/', admin.site.urls),
]
