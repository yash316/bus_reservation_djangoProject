from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Bus, Booking


# Create your views here.

class Index(View):
    def get(self, request):
        return render(request, 'index.html')


class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        print(first_name, last_name)
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None
        user = User(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                    password=password)
        # validations
        if (not first_name):
            error_message = "First name is required."
        elif (not last_name):
            error_message = "Last name is required."
        elif (not phone):
            error_message = "Phone Number is required."
        elif len(phone) < 10:
            error_message = "Phone number should be of 10 digits."
        elif (not password):
            error_message = "Password is required."
        elif len(password) < 6:
            error_message = "Password should be 6 character long."
        elif (not confirm_password):
            error_message = "Confirm Password is required."
        elif (not password == confirm_password):
            error_message = "Password and Confirm Password should be same."
        elif user.isExists():
            error_message = 'Email Address Already Exists.'
            # saving
        if not error_message:
            user.password = make_password(user.password)
            user.save()
            return redirect('Home')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        # print(email, password)
        user = User.get_customer_by_email(email)
        error_message = None
        if user:
            flag = check_password(password, user.password)
            if flag:
                request.session['customer'] = user.id
                request.session['email'] = user.email
                return redirect('Home')
            else:
                error_message = "Email or Password Invalid."
        else:
            error_message = "Email or Password Invalid."
        return render(request, 'login.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('Login')


class Search_bus(View):
    def get(self, request):
        if request.method == 'GET':
            buses = Bus.objects.all()
            src = request.GET.get('source')
            dest = request.GET.get('dest')
            date = request.GET.get('date')
        if src != None:
            busss = Bus.objects.filter(source__icontains=src, destination__icontains=dest, date__icontains=date)
            return render(request, 'buses.html', {'result': busss})
        return render(request, 'buses.html')

    def post(self, request):

        busid = request.POST.get('busid')
        nos = request.POST.get('no_seats')
        bus = Bus.objects.get(id=busid)
        if bus:
            user = request.session.get('customer')
            b_name = bus.bus_Name
            nos = request.POST.get('no_seats')
            contact = request.POST.get('contact')
            cost = int(nos) * bus.price
            b_from = bus.source
            b_dest = bus.destination
            price = bus.price
            b_date = bus.date
            b_time = bus.time

            Book = Booking(user=User(id=user),
                           Bus_Name=b_name,
                           No_Seats=nos,
                           Contact=contact,
                           From=b_from,
                           To=b_dest,
                           Price_Per_Ticket=price,
                           Cost=cost,
                           T_date=b_date,
                           T_time=b_time, )
            Book.save()
            return render(request, 'success.html',{
                'User': User(id=user),
                'Bus_Name':b_name,
                'nos':nos,
                'contact':contact,
                'source':b_from,
                'dest':b_dest,
                'ppt': price,
                'cost':cost,
                'tdate':b_date,
                'ttime':b_time
            })

        return render(request, 'buses.html')


class SeeBooking(View):

    def get(self, request):
        customer = request.session.get('customer')
        booking = Booking.get_orders_by_customer(customer)
        # print(orders)
        return render(request, 'bookings.html', {'booking': booking})
