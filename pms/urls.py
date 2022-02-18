from django.urls import path
from . import views_

urlpatterns=[
    path("",views_.home,name="home"),
    path("search/room/",views_.room_search,name="search"),
    path("search/book/",views_.book_search,name="book_search"),
    path("book/<str:pk>/",views_.book,name="book"),
    path("reservations/",views_.reservations,name="reservations")
]