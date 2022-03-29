import uuid
import requests
import json

from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

from . forms import SignupForm
from.models import Category, Rooms, Reservation, Payment
# create your views 

def password(request):
    update = PasswordChangeForm(request.user)
    if request.method == 'POST':
        update = PasswordChangeForm(request.user, request.POST)
        if update.is_valid():
            user=update.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password update successful!')
            return redirect('index')
        else:
            messages.error(request, update.errors)
            return redirect('password')

    context = {
        'update': update
    }

    return render(request, 'password.html', context)

def loginpage(request):  
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            login(request, user)
            messages.success(request, 'successful')
            return redirect('index')
        else:
            messages.info(request, 'username/password incorrect')
            return redirect('login')

    return render (request, 'login.html')

def logoutfunc(request):
    logout(request)
    return redirect('login')

def signupform(request):
    reg = SignupForm()
    if request.method == 'POST':
        reg = SignupForm(request.POST)
        if reg.is_valid():
            new = reg.save()
            login(request, new)
            messages.success(request, 'Signup successfull!')
            return redirect('index')
        else:
            messages.warning(request, reg.errors)
            return redirect('signupform')

    context = {
        'reg': reg
    }

    return render (request,'signup.html', context)

def gym(request):
    return render(request, 'gym.html')

def explore(request):
    return render(request, 'explore.html')

def contact(request):
    return render(request, 'contact.html')

def index(request):
    categories = Category.objects.all()

    context={
        'categories': categories,
    }

    return render(request, 'index.html',context)

def categories(request):
    categories = Category.objects.all()
    
    context={
        'categories': categories
    }

    return render(request, 'categories.html', context)

def rooms(request):
    available= Rooms.objects.all().filter(available=True)
   
    context={
        'available': available,
    }

    return render(request, 'rooms.html',context) 

def category(request,id):
    categories = Category.objects.all()
    classroom = Rooms.objects.filter(category_id=id)
    room = Category.objects.get(pk=id)
    
    context={
        'room': room,
        'classroom': classroom,
    }

    return render(request, 'category.html',context)

def room(request,id):
    room = Rooms.objects.get(pk=id)

    context={
        'room': room,
    }
    
    return render(request, 'room.html', context)

@login_required(login_url='/login')
def addtocart(request):
    if request.method == 'POST':
        refrence = str(uuid.uuid4())
        pid = request.POST['itemid']
        checkout = request.POST['check_out']
        checkin = request.POST['check_in']
        item = Rooms.objects.get(pk=pid)
        reservation = Reservation.objects.filter(user__username= request.user.username, paid_order=False)
        if reservation:
            order = Reservation.objects.filter(user__username=request.user.username, room_id=item.id,check_in = checkin,check_out = checkout).first()
            if order:
                order.check_in = checkin
                order.check_out = checkout
                if order.check_in > checkout or order.check_out < checkin:
                    order.save()
                    messages.success(request, 'Your booking is successful!')
                else:
                    messages.info(request, 'The room is not available for the dates you specified, kindly choose another date. Thank you')
                    return redirect('rooms')
                
            else:
                    # this runs when a new item is added to the basket 
                newitem = Reservation()
                newitem.user = request.user
                newitem.room =item
                newitem.order_no = reservation[0].order_no
                newitem.paid_order = False
                newitem.description = item.description
                newitem.check_in = checkin
                newitem.check_out = checkout
                newitem.save() 
                messages.success(request, 'Room added to bookings !')           
        else:
            # this is when a basket is to be created for the first time 
            newbasket = Reservation()
            newbasket.user = request.user
            newbasket.room =item
            newbasket.order_no = refrence
            newbasket.paid_order = False
            newbasket.description = item.description
            newbasket.check_in = checkin
            newbasket.check_out = checkout
            newbasket.save() 
            messages.success(request, 'Room added to bookings !')
    return redirect('reservation')

@login_required(login_url='/login')
def reservation(request):
    reservation = Reservation.objects.filter(user__username=request.user.username, paid_order=False)
    
    for item in reservation:
        time = (item.check_out - item.check_in).days
        item.nights = time
        item.save()
        

    subtotal=0
    vat=0
    total=0

    for item in reservation:
        subtotal += item.room.price * item.nights 

    vat=0.075 *subtotal

    total=subtotal + vat

    context={
        'reservation':reservation,
        'subtotal':subtotal,
        'vat':vat,
        'total':total
    }
    return render(request, 'reservation.html',context)

@login_required(login_url='/login')
def checkout(request):
    reservation = Reservation.objects.filter(user__username = request.user.username,paid_order=False)
 
    for item in reservation:
        time = (item.check_out - item.check_in).days
        item.nights = time
        item.save()

    subtotal = 0
    vat = 0
    total = 0

    for item in reservation:
        subtotal += item.room.price * item.nights

    vat = 0.075 * subtotal

    total = subtotal + vat


    context = {
        'reservation': reservation,
        'total': total,
        'subtotal': subtotal,
        'reservation_code':reservation[0].order_no
    }

    return render(request, 'checkout.html', context)

@login_required(login_url='/login')
def deleteitem(request):
    itemid=request.POST['itemid']
    Reservation.objects.filter(pk=itemid).delete()
    messages.success(request, 'room deleted')
    return redirect('reservation')

@login_required(login_url='/login')
def increase(request):
    check_in=request.POST['check_in']
    check_out=request.POST['check_out']
    valid=request.POST['valid']
    updates =Reservation.objects.get(pk=valid)
    
    updates.check_in =check_in
    updates.check_out =check_out
    if  updates.check_in > check_out or updates.check_out < check_in:
        updates.save()
        messages.success(request, 'Your booking dates update is successful!')
    else:
        messages.info(request, 'The room is not available for the dates you specified, kindly choose another date. Thank you')
        return redirect('rooms')
    
    return redirect('reservation')

@login_required(login_url='/login')
def placeorder(request):
    if request.method == 'POST':
        api_key = 'sk_test_9f72c94a11fc5b98c9d69e66a128c2db475dc288'
        curl = 'https://api.paystack.co/transaction/initialize'
        cburl = 'http://44.201.133.147/completed'
        # cburl= 'http://localhost:8000/completed/'
        total = float(request.POST['total']) * 100
        reservation_code = request.POST['reservation_code']
        pay_code = str(uuid.uuid4())
        user = User.objects.get(username=request.user.username)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        
        # collect data that you will send to paystack
        headers = {'Authorization': f'Bearer {api_key}'}
        data = {'reference': pay_code, 'email': user.email,'amount':int(total), 'callback_url': cburl, 'order_number': reservation_code}

        # make a call to paystack
        try:
            r = requests.post(curl, headers=headers, json=data)
        except Exception:
            messages.error(request, 'Network busy, try again')
        else:
            transback = json.loads(r.text)
            rd_url = transback['data']['authorization_url']

            paid = Payment()
            paid.user = user
            paid.amount = total
            paid.order_no = reservation_code
            paid.pay_code = pay_code
            paid.paid_order = True
            paid.first_name = first_name  
            paid.last_name = last_name
            paid.phone = phone
            paid.save()

            reserve = Reservation.objects.filter(user__username=request.user, paid_order=False)
            for item in reserve:
                item.paid_order = True
                item.amount = total/100
                item.save()

                book = Rooms.objects.get(pk=item.room.id)
                book.paid_order = True
                book.available = False
                book.booked = True
                book.save()
            
            return redirect(rd_url)
    return redirect('checkout')

def completed(request):
    client = User.objects.get(username=request.user.username)
    pay = Reservation.objects.filter(user__username=request.user.username, paid_order=True)

    context={
        'client':client,
        'pay':pay,
       
    }

    return render(request, 'completed.html', context)


def history(request):
    client = User.objects.get(username=request.user.username)
    pay = Reservation.objects.filter(user__username=request.user.username, paid_order=True)

    context={
        'client':client,
        'pay':pay,
       
    }
    return render(request, 'history.html', context)