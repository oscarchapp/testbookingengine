from urllib import request
from django.shortcuts import render, redirect
from django.views import View
from .models import Room
from .forms import *
from django.db.models import F,Q, Count
from .reservation_code import generate
from .form_dates import Ymd
from django.views.decorators.csrf import ensure_csrf_cookie
# Create your views here.

class BookSearchView(View):

    def get(self,request):
        query=request.GET.dict()
        if(not "filter" in query):
            return redirect("/")
        books=(Book.objects
            .filter(Q(code__icontains=query['filter']) | Q(customer__name__icontains=query['filter']))
            .order_by("-created"))
        room_search_form=RoomSearchForm()
        context={
            'books':books,
            'form':room_search_form
        }
        return render(request,"home.html",context)


class RoomSearchView(View):
    def get(self,request):
        query=request.GET.dict()
        checkin=Ymd.Ymd(query['checkin'])
        checkout=Ymd.Ymd(query['checkout'])
        total_days=checkout-checkin

        filters={
            'room_type__max_guests__gte':query['guests']
            }
        exclude={
            'book__checkin__lte':query['checkout'],
            'book__checkout__gte':query['checkin'],
            }
        rooms=(Room.objects
            .filter(**filters)
            .exclude(**exclude)
            .annotate(total=total_days*F('room_type__price'))
            .order_by("room_type__max_guests","name")
            )
        total_rooms=(Room.objects
            .filter(**filters)
            .values("room_type__name","room_type")
            .exclude(**exclude)
            .annotate(total=Count('room_type'))
            .order_by("room_type__max_guests"))
        data={
            'total_days':total_days
        }
        url_query=request.GET.urlencode()
        context={
            "rooms":rooms,
            "total_rooms":total_rooms,
            "query":query,
            "url_query":url_query,
            "data":data
            }
        return render(request,"search.html",context)

class HomeView(View):
    def get(self,request):
        books=Book.objects.all().order_by("-created")
        room_search_form=RoomSearchForm()
        context={
            'books':books,
            'form':room_search_form
        }
        return render(request,"home.html",context)

class BookView(View):
    from django.utils.decorators import method_decorator
    @method_decorator(ensure_csrf_cookie)

    def post(self, request,pk):
        customer_form=CustomerForm(request.POST,prefix="customer")
        if customer_form.is_valid():
            customer=customer_form.save()
            temp_POST=request.POST.copy()
            temp_POST.update({
                'book-customer':customer.id,
                'book-room':pk,
                'book-code':generate.get()})
            book_form=BookForm(temp_POST,prefix="book")
            if book_form.is_valid():
                book_form.save()
                
        return redirect('/')

    def get(self,request,pk):
        query=request.GET.dict()
        room=Room.objects.get(id=pk)
        checkin=Ymd.Ymd(query['checkin'])
        checkout=Ymd.Ymd(query['checkout'])
        total_days=checkout-checkin
        total=total_days*room.room_type.price
        print(total)
        query['total']=total
        context={
            "url_query":request.GET.urlencode(),
            "room":room,
            "book_form":BookFormExcluded(prefix="book",initial=query),
            "customer_form":CustomerForm(prefix="customer")
            }
        return render(request,"book.html",context)

    


def reservations(request):
    return render(request,"reservations.html")