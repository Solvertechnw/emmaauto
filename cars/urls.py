from django.urls import path
from . import views

app_name = "cars"

urlpatterns = [
    path("", views.home, name="home"),  # homepage
    path("list/", views.car_list, name="list"),  # car list page
     path("contact/", views.contact_view, name="contact"),  # contact
    path("<slug:slug>/", views.car_detail, name="detail"),  # car detail
   
]
