from django.urls import path
from . import views_

urlpatterns = [
    path("",views_.HomeView.as_view(),name = "home"),
    path("search/room/",views_.RoomSearchView.as_view(),name = "search"),
    path("search/booking/",views_.BookingSearchView.as_view(),name = "booking_search"),
    path("booking/<str:pk>/",views_.BookingView.as_view(),name = "booking"),
    path("booking/<str:pk>/edit",views_.EditBookingView.as_view(),name = "edit_booking"),
    path("booking/<str:pk>/delete",views_.DeleteBookingView.as_view(),name = "delete_booking"),
    path("dashboard/",views_.DashboardView.as_view(),name = "dashboard")
]