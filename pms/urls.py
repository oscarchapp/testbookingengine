from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("search/room/", views.RoomSearchView.as_view(), name="search"),
    path("search/booking/", views.BookingSearchView.as_view(), name="booking_search"),
    path("booking/<str:pk>/", views.BookingView.as_view(), name="booking"),
    path("booking/<str:pk>/edit", views.EditBookingView.as_view(), name="edit_booking"),
    path("booking/<str:pk>/edit-dates", views.EditBookingDatesView.as_view(), name="edit_booking_dates"),
    path("booking/<str:pk>/delete", views.DeleteBookingView.as_view(), name="delete_booking"),
    path("rooms/", views.RoomsView.as_view(), name="rooms"),
    path("room/<str:pk>/", views.RoomDetailsView.as_view(), name="room_details"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard")
]
