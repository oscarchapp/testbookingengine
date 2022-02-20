from urllib import request
from django.shortcuts import render, redirect
from django.views import View
from .models import Room
from .forms import *
from django.db.models import F,Q, Count
from .reservation_code import generate
from .form_dates import Ymd
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
# Create your views here.

class BookSearchView(View):

    def get(self,request):
        query = request.GET.dict()
        if(not "filter" in query):
            return redirect("/")
        books = (Book.objects
            .filter(Q(code__icontains = query['filter']) | Q(customer__name__icontains = query['filter']))
            .order_by("-created"))
        room_search_form = RoomSearchForm()
        context = {
            'books':books,
            'form':room_search_form
        }
        return render(request,"home.html",context)


class RoomSearchView(View):
    #renders the search form
    def get(self,request):
        room_search_form = RoomSearchForm()
        context = {
            'form':room_search_form
        }
        
        return render(request,"book_search_form.html",context)

    #renders the search results of available rooms by date and guests
    def post(self,request):
        query = request.POST.dict()
        #calculate number of days in the hotel
        checkin = Ymd.Ymd(query['checkin'])
        checkout = Ymd.Ymd(query['checkout'])
        total_days = checkout-checkin
        #get available rooms and total according to dates and guests
        filters = {
            'room_type__max_guests__gte':query['guests']
            }
        exclude = {
            'book__checkin__lte':query['checkout'],
            'book__checkout__gte':query['checkin'],
            }
        rooms = (Room.objects
            .filter(**filters)
            .exclude(**exclude)
            .annotate(total = total_days*F('room_type__price'))
            .order_by("room_type__max_guests","name")
            )
        total_rooms = (Room.objects
            .filter(**filters)
            .values("room_type__name","room_type")
            .exclude(**exclude)
            .annotate(total = Count('room_type'))
            .order_by("room_type__max_guests"))
        #prepare context data for template
        data = {
            'total_days':total_days
        }
        #pass the actual url query to the template
        url_query = request.POST.urlencode()
        context = {
            "rooms":rooms,
            "total_rooms":total_rooms,
            "query":query,
            "url_query":url_query,
            "data":data
            }
        return render(request,"search.html",context)

class HomeView(View):
    #renders home page with all the books order by date of creation
    def get(self,request):
        books = Book.objects.all().order_by("-created")
        context = {
            'books':books
        }
        return render(request,"home.html",context)

class BookView(View):
    @method_decorator(ensure_csrf_cookie)
    def post(self, request,pk):
        #check if customer form is ok
        customer_form = CustomerForm(request.POST,prefix = "customer")
        if customer_form.is_valid():
            #save customer data
            customer = customer_form.save()
            #add the customer id to the book form
            temp_POST = request.POST.copy()
            temp_POST.update({
                'book-customer':customer.id,
                'book-room':pk,
                'book-code':generate.get()})
            #if ok, save book data
            book_form = BookForm(temp_POST,prefix = "book")
            if book_form.is_valid():
                book_form.save()
                
        return redirect('/')

    def get(self,request,pk):
        #renders the form for book confirmation. 
        # It returns 2 forms, the one with the book info is hidden
        #The second form is for the customer information

        query = request.GET.dict()
        room = Room.objects.get(id = pk)
        checkin = Ymd.Ymd(query['checkin'])
        checkout = Ymd.Ymd(query['checkout'])
        total_days = checkout-checkin
        total = total_days*room.room_type.price #total amount to be paid
        query['total'] = total
        url_query = request.GET.urlencode()
        book_form = BookFormExcluded(prefix = "book",initial = query)
        customer_form = CustomerForm(prefix = "customer")
        context = {
            "url_query":url_query,
            "room":room,
            "book_form":book_form,
            "customer_form":customer_form
            }
        return render(request,"book.html",context)

class EditBookView(View):
    #renders the customer edition form
    def get(self,request,pk):

        book = Book.objects.get(id=pk)
        book_form = BookForm(prefix="book",instance=book)
        customer_form = CustomerForm(prefix="customer",instance=book.customer)
        context = {
            'book_form':book_form,
            'customer_form':customer_form

        }
        return render(request,"edit_book.html",context)


    #updates the customer form
    @method_decorator(ensure_csrf_cookie)
    def post(self,request,pk):
        book = Book.objects.get(id=pk)
        customer_form = CustomerForm(request.POST,prefix = "customer",instance=book.customer)
        if customer_form.is_valid():
            print(customer_form)
            customer_form.save()
            return redirect("/")

        pass
    


def reservations(request):
    return render(request,"reservations.html")