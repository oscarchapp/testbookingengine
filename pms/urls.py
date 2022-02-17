from django.urls import path
from . import views_

urlpatterns=[
    path("",views_.home,name="home"),
    path("search/",views_.search,name="search"),
    path("book/<str:pk>/",views_.book,name="book"),
    path("reservations/",views_.reservations,name="reservations")
]