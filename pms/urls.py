from django.urls import path
from . import views_

urlpatterns = [
    path("",views_.HomeView.as_view(),name = "home"),
    path("search/room/",views_.RoomSearchView.as_view(),name = "search"),
    path("search/book/",views_.BookSearchView.as_view(),name = "book_search"),
    path("book/<str:pk>/",views_.BookView.as_view(),name = "book"),
    path("book/<str:pk>/edit",views_.EditBookView.as_view(),name = "edit_book"),
    path("reservations/",views_.reservations,name = "reservations")
]