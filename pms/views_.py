from datetime import date
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from .models import Room
from .forms import *
from datetime import datetime
from django.db.models import F
from .reservation_code import generate
# Create your views here.

def search(request):
    query=request.GET.dict()
    date_format = "%Y-%m-%d"
    a = datetime.strptime(query['checkin'], date_format)
    b = datetime.strptime(query['checkout'], date_format)
    total_days=(b-a).days

    filters={
        'room_type__max_guests__gte':query['guests']
        }
    exclude={
        'book__checkin__lte':query['checkout'],
        'book__checkout__gte':query['checkin'],
        }
    rooms=Room.objects.filter(
            **filters
        ).exclude(
            **exclude
        ).annotate(total=total_days*F('room_type__price'))
    data={
        'total_days':total_days
    }
    query=request.GET.urlencode()
    context={
        "rooms":rooms,
        "query":query,
        "data":data
        }
    return render(request,"search.html",context)


def home(request):
    books=Book.objects.all().order_by("-created")
    context={
        'books':books
    }
    print(books)
    return render(request,"home.html",context)


def book(request,pk):
    if(request.method=="POST"):
        customer_form=CustomerForm(request.POST,prefix="customer")
        if customer_form.is_valid():
            body=request.POST.dict()
            customer=customer_form.save(commit=True)
            temp_POST=request.POST.copy()
            temp_POST.update({
                'book-customer':customer.id,
                'book-room':pk,
                'book-code':generate.get()})
            book_form=BookForm(temp_POST,prefix="book")
            
            if book_form.is_valid():
                pass
                book_form.save(commit=True)
                
        return redirect('/')
    query=request.GET.dict()
    room=Room.objects.get(id=pk)
    date_format = "%Y-%m-%d"
    a = datetime.strptime(query['checkin'], date_format)
    b = datetime.strptime(query['checkout'], date_format)
    total_days=(b-a).days
    total=total_days*room.room_type.price
    print(total)
    query['total']=total
    context={
        "room":room,
        "book_form":BookFormExcluded(prefix="book",initial=query),
        "customer_form":CustomerForm(prefix="customer")
        }
    return render(request,"book.html",context)


def reservations(request):
    return render(request,"reservations.html")