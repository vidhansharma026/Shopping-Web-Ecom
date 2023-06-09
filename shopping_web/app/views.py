from django.shortcuts import render,redirect
from . models import *
from django.views import View
from django.db.models import Q
from django.http import JsonResponse
# from .forms import CustomerRegistrationForm, CustomerProfileForm

# def home(request):
#  return render(request, 'app/home.html')

# def product_detail(request):
#  products = Product.objects.all()       
#  context = {'products' : products}
#  return render(request, 'app/productdetail.html',context)

# def add_to_cart(request):
#  return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 states = Customer.objects.all()
 return render(request, 'app/profile.html',{'states': states})

def address(request):
 return render(request, 'app/address.html')

def orders(request):
 return render(request, 'app/orders.html')

def change_password(request):
 return render(request, 'app/changepassword.html')

# def electronics(request):
#  return render(request, 'app/electronics.html')

def login(request):
 return render(request, 'app/login.html')

def customerregistration(request):
 return render(request, 'app/customerregistration.html')

def checkout(request):
 return render(request, 'app/checkout.html')


class ProductView(View):
 def get(self, request):
  topwears = Product.objects.filter(category = 'TW')
  bottomwears = Product.objects.filter(category = 'BW')
  electronics = Product.objects.filter(category = 'E')
  accesories = Product.objects.filter(category = 'A')
  return render(request, 'app/home.html',{'topwears':topwears, 'bottomwears':bottomwears, 'electronics':electronics, 'accesories':accesories})
 
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()
            return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart})
        else:
            return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart})

def add_to_cart(request):
  user = request.user
  product_id = request.GET.get('prod_id')
  product = Product.objects.get(id = product_id)
  Cart(user = user, product = product).save()
  return redirect('/cart/')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        actual_amount = 0.0
        discount_amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                discamount = (p.quantity*p.product.discounted_price)
                sellamount = (p.quantity*p.product.selling_price)
                discount_amount += discamount
                actual_amount += sellamount
                total_amount = discount_amount+shipping_amount
            return render(request, 'app/addtocart.html', {'carts': cart, 'total_amount': total_amount, 'actual_amount': actual_amount, 'discount_amount':discount_amount})
        else:
            return render(request, 'app/emptycart.html')
        
def electronic(request, data=None):
    if data == None:
        electronic = Product.objects.filter(category='E')
    elif data == 'Apple' or data == 'hp':
        electronic = Product.objects.filter(category='E').filter(brand=data)
    elif data == 'below':
        electronic = Product.objects.filter(
            category='E').filter(discounted_price__lt=10000)
    elif data == 'above':
        electronic = Product.objects.filter(
            category='E').filter(discounted_price__gt=10000)
    return render(request, 'app/electronic.html', {'electronic': electronic})

def accesories(request, data=None):
    if data == None:
        accesories = Product.objects.filter(category='A')
    elif data == 'godfather' or data == 'oliva':
        accesories = Product.objects.filter(category='A').filter(brand=data)
    elif data == 'below':
        accesories = Product.objects.filter(
            category='A').filter(discounted_price__lt=25000)
    elif data == 'above':
        accesories = Product.objects.filter(
            category='A').filter(discounted_price__gt=25000)
    return render(request, 'app/accesories.html', {'accesories': accesories})

def topwears(request, data=None):
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'ZARA' or data == 'GUCCI':
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    elif data == 'below':
        topwears = Product.objects.filter(
            category='TW').filter(discounted_price__lt=1000)
    elif data == 'above':
        topwears = Product.objects.filter(
            category='TW').filter(discounted_price__gt=1000)
    return render(request, 'app/topwear.html', {'topwears': topwears})

def bottomwears(request, data=None):
    if data == None:
        bottomwears = Product.objects.filter(category='BW')
    elif data == 'ZARA' or data == 'GUCCI':
        bottomwears = Product.objects.filter(category='BW').filter(brand=data)
    elif data == 'below':
        bottomwears = Product.objects.filter(
            category='BW').filter(discounted_price__lt=1000)
    elif data == 'above':
        bottomwears = Product.objects.filter(
            category='BW').filter(discounted_price__gt=1000)
    return render(request, 'app/bottomwear.html', {'bottomwears': bottomwears})

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        discount_amount = 0.0
        actual_amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            discamount = (p.quantity * p.product.discounted_price)
            sellamount = (p.quantity*p.product.selling_price)
            discount_amount += discamount
            actual_amount += sellamount
        data = {
            'quantity': c.quantity,
            'discount_amount': discount_amount,
            'actual_amount': actual_amount,
            'totalamount': discount_amount + shipping_amount
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        discount_amount = 0.0
        actual_amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            discamount = (p.quantity * p.product.discounted_price)
            sellamount = (p.quantity*p.product.selling_price)
            discount_amount += discamount
            actual_amount += sellamount

        data = {
            'quantity': c.quantity,
            'discount_amount': discount_amount,
            'actual_amount': actual_amount,
            'totalamount': discount_amount + shipping_amount
        }
        return JsonResponse(data)

# class ProfileView(View):
#     def get(self, request):
#         form = CustomerProfileForm()
#         return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        discount_amount = 0.0
        actual_amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            discamount = (p.quantity * p.product.discounted_price)
            sellamount = (p.quantity * p.product.selling_price)
            discount_amount += discamount
            actual_amount += sellamount

        data = {
            'discount_amount': discount_amount,
            'actual_amount': actual_amount,
            'totalamount': discount_amount + shipping_amount
        }
        return JsonResponse(data)

# from itertools import product
# from statistics import quantiles
# from django.http import JsonResponse
# from django.shortcuts import redirect, render
# from django.views import View
# from .models import Customer, Product, Cart, OrderPlaced
# from .forms import CustomerRegistrationForm, CustomerProfileForm
# from django.contrib import messages
# from django.db.models import Q
# from django.http import JsonResponse
# from django.http import HttpResponse
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from django.contrib.auth.models import User

# # def home(request):
# #  return render(request, 'app/home.html')


# class ProductView(View):
#     def get(self, request):
#         topwears = Product.objects.filter(category='TW')
#         bottomwears = Product.objects.filter(category='BW')
#         mobiles = Product.objects.filter(category='M')
#         laptops = Product.objects.filter(category='L')
#         return render(request, 'app/home.html',
#                       {'topwears': topwears, 'bottomwears': bottomwears, 'mobiles': mobiles, "laptops": laptops})


# # def product_detail(request):
# #  return render(request, 'app/productdetail.html')
# class ProductDetailView(View):
#     def get(self, request, pk):
#         product = Product.objects.get(pk=pk)
#         item_already_in_cart = False
#         if request.user.is_authenticated:
#             item_already_in_cart = Cart.objects.filter(
#                 Q(product=product.id) & Q(user=request.user)).exists()
#             return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart})
#         else:
#             return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart})


# @login_required
# def add_to_cart(request):
#     user = request.user
#     product_id = request.GET.get('prod_id')
#     product = Product.objects.get(id=product_id)
#     Cart(user=user, product=product).save()
#     return redirect('/cart')


# @login_required
# def show_cart(request):
#     if request.user.is_authenticated:
#         user = request.user
#         cart = Cart.objects.filter(user=user)
#         amount = 0.0
#         shipping_amount = 70.0
#         total_amount = 0.0
#         cart_product = [p for p in Cart.objects.all() if p.user == user]
#         print(cart_product)
#         if cart_product:
#             for p in cart_product:
#                 tempamount = (p.quantity*p.product.discounted_price)
#                 amount += tempamount
#                 total_amount = amount+shipping_amount
#             return render(request, 'app/addtocart.html', {'carts': cart, 'total_amount': total_amount, 'amount': amount})
#         else:
#             return render(request, 'app/emptycart.html')


# @login_required
# def plus_cart(request):
#     if request.method == 'GET':
#         prod_id = request.GET['prod_id']
#         c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
#         c.quantity += 1
#         c.save()
#         amount = 0.0
#         shipping_amount = 70.0
#         cart_product = [p for p in Cart.objects.all() if p.user ==
#                         request.user]
#         for p in cart_product:
#             tempamount = (p.quantity * p.product.discounted_price)
#             amount += tempamount

#         data = {
#             'quantity': c.quantity,
#             'amount': amount,
#             'totalamount': amount + shipping_amount
#         }
#         return JsonResponse(data)


# @login_required
# def minus_cart(request):
#     if request.method == 'GET':
#         prod_id = request.GET['prod_id']
#         c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
#         c.quantity -= 1
#         c.save()
#         amount = 0.0
#         shipping_amount = 70.0
#         cart_product = [p for p in Cart.objects.all() if p.user ==
#                         request.user]
#         for p in cart_product:
#             tempamount = (p.quantity * p.product.discounted_price)
#             amount += tempamount

#         data = {
#             'quantity': c.quantity,
#             'amount': amount,
#             'totalamount': amount + shipping_amount
#         }
#         return JsonResponse(data)


# @login_required
# def remove_cart(request):
#     if request.method == 'GET':
#         prod_id = request.GET['prod_id']
#         c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
#         c.delete()
#         amount = 0.0
#         shipping_amount = 70.0
#         cart_product = [p for p in Cart.objects.all() if p.user ==
#                         request.user]
#         for p in cart_product:
#             tempamount = (p.quantity * p.product.discounted_price)
#             amount += tempamount

#         data = {
#             'amount': amount,
#             'totalamount': amount + shipping_amount
#         }
#         return JsonResponse(data)


# @login_required
# def buy_now(request):
#     return render(request, 'app/buynow.html')

# # def profile(request):
# #  return render(request, 'app/profile.html')


# @login_required
# def address(request):
#     add = Customer.objects.filter(user=request.user)
#     return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})


# @login_required
# def orders(request):
#     op = OrderPlaced.objects.filter(user=request.user)
#     return render(request, 'app/orders.html', {'order_placed': op})

# # def change_password(request):
# #  return render(request, 'app/changepassword.html')


# def mobile(request, data=None):
#     if data == None:
#         mobiles = Product.objects.filter(category='M')
#     elif data == 'Redmi' or data == 'Samsung':
#         mobiles = Product.objects.filter(category='M').filter(brand=data)
#     elif data == 'below':
#         mobiles = Product.objects.filter(
#             category='M').filter(discounted_price__lt=10000)
#     elif data == 'above':
#         mobiles = Product.objects.filter(
#             category='M').filter(discounted_price__gt=10000)
#     return render(request, 'app/mobile.html', {'mobiles': mobiles})


# def laptop(request, data=None):
#     if data == None:
#         laptops = Product.objects.filter(category='L')
#     elif data == 'Asus' or data == 'Dell':
#         laptops = Product.objects.filter(category='L').filter(brand=data)
#     elif data == 'below':
#         laptops = Product.objects.filter(
#             category='L').filter(discounted_price__lt=25000)
#     elif data == 'above':
#         laptops = Product.objects.filter(
#             category='L').filter(discounted_price__gt=25000)
#     return render(request, 'app/laptop.html', {'laptops': laptops})


# def topwear(request, data=None):
#     if data == None:
#         topwears = Product.objects.filter(category='TW')
#     elif data == 'ZARA' or data == 'GUCCI':
#         topwears = Product.objects.filter(category='TW').filter(brand=data)
#     elif data == 'below':
#         topwears = Product.objects.filter(
#             category='TW').filter(discounted_price__lt=1000)
#     elif data == 'above':
#         topwears = Product.objects.filter(
#             category='TW').filter(discounted_price__gt=1000)
#     return render(request, 'app/topwear.html', {'topwears': topwears})


# def bottomwear(request, data=None):
#     if data == None:
#         bottomwears = Product.objects.filter(category='BW')
#     elif data == 'ZARA' or data == 'GUCCI':
#         bottomwears = Product.objects.filter(category='BW').filter(brand=data)
#     elif data == 'below':
#         bottomwears = Product.objects.filter(
#             category='BW').filter(discounted_price__lt=1000)
#     elif data == 'above':
#         bottomwears = Product.objects.filter(
#             category='BW').filter(discounted_price__gt=1000)
#     return render(request, 'app/bottomwear.html', {'bottomwears': bottomwears})


# # def login(request):
# #  return render(request, 'app/login.html')

# # def customerregistration(request):
# #  return render(request, 'app/customerregistration.html')

# class CustomerRegistrationView(View):
#     def get(self, request):
#         form = CustomerRegistrationForm()
#         return render(request, 'app/customerregistration.html', {'form': form})

#     def post(self, request):
#         form = CustomerRegistrationForm(request.POST)
#         if form.is_valid():
#             messages.success(
#                 request, 'Congratulation!! Registered Successfully')
#             form.save()
#         return render(request, 'app/customerregistration.html', {'form': form})


# @login_required
# def checkout(request):
#     user = request.user
#     add = Customer.objects.filter(user=user)
#     cart_items = Cart.objects.filter(user=user)
#     amount = 0.0
#     shipping_amount = 70.0
#     totalamount = 0.0
#     cart_product = [p for p in Cart.objects.all() if p.user == request.user]
#     if cart_product:
#         for p in cart_product:
#             tempamount = (p.quantity * p.product.discounted_price)
#             amount += tempamount
#         totalamount = amount + shipping_amount
#     return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalamount, 'cart_items': cart_items})


# @login_required
# def payment_done(request):
#     user = request.user
#     custid = request.GET.get('custid')
#     customer = Customer.objects.get(id=custid)
#     cart = Cart.objects.filter(user=user)
#     for c in cart:
#         OrderPlaced(user=user, customer=customer,
#                     product=c.product, quantity=c.quantity).save()
#         c.delete()
#     return redirect("orders")


# class ProfileView(View):
#     def get(self, request):
#         form = CustomerProfileForm()
#         return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

#     def post(self, request):
#         form = CustomerProfileForm(request.POST)
#         if form.is_valid():
#             usr = request.user
#             name = form.cleaned_data['name']
#             locality = form.cleaned_data['locality']
#             city = form.cleaned_data['city']
#             state = form.cleaned_data['state']
#             zipcode = form.cleaned_data['zipcode']
#             reg = Customer(user=usr, name=name, locality=locality,
#                            city=city, state=state, zipcode=zipcode)
#             reg.save()
#             messages.success(
#                 request, 'Congratulation!! Profile Updated Succesfully')
#         return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})