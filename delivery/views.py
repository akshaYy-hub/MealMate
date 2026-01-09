from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.shortcuts import redirect, get_object_or_404
from .models import Cart, CartItem, Item, User
import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User



from .models import User, Restaurant, Item, Cart
from .models import CartItem
from .models import User, Restaurant, Item, Cart, CartItem


import razorpay
from django.conf import settings

# Create your views here.
def index(request):
    return render(request, 'index.html')

def open_signin(request):
    return render(request, 'signin.html')

def open_signup(request):
    return render(request, 'signup.html')

# def signin(request):
#     #DB's Data
#     user = "gamana"
#     pw = "123"
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         if user == username and pw == password:
#             # return HttpResponse(f"Username : {username} password : {password}")
#             return render(request, "success.html") 
#         else:
#             #return HttpResponse(f"Invalid response")
#             return render(request, "fail.html") 
    
#     else:
#         return HttpResponse("Invalid Request")

# def signin(request):
#     if request.method == 'POST':
#         # Fetching data from the form
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         try:
#             # Check if a user exists with the provided credentials
#             customer = User.objects.get(username=username, password=password)
#             return render(request, 'success.html')
#         except User.DoesNotExist:
#             # If credentials are invalid, show a failure page
#             return render(request, 'fail.html')
#     else:
#         return HttpResponse("Invalid Request")

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login

def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("open_show_restaurant")
    

            return render(request, "signin.html", {
            "error": "Invalid username or password"
        })

    return render(request, "signin.html")


        
from django.contrib.auth.models import User

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Username already exists"
            })

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        user.save()

        return redirect("open_signin")

    return render(request, "signup.html")


   

    
def open_add_restaurant(request):
    return render(request, 'add_restaurant.html')

def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
        
        try:
            Restaurant.objects.get(name = name)
            return HttpResponse("Duplicate restaurant!")
            
        except:
            Restaurant.objects.create(
                name = name,
                picture = picture,
                cuisine = cuisine,
                rating = rating,
            )
    # return HttpResponse("Successfully Added !")
        return render(request, 'admin_home.html')


def open_show_restaurant(request):

    restaurantList = Restaurant.objects.all()
    return render(request, 'show_restaurants.html',{"restaurantList" : restaurantList})

def open_update_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    return render(request, 'update_restaurant.html', {"restaurant" : restaurant})

def update_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')

        restaurant.name = name
        restaurant.picture = picture
        restaurant.cuisine = cuisine
        restaurant.rating = rating
        restaurant.save()

        return redirect('open_show_restaurant')

    restaurantList = Restaurant.objects.all()
    return render(request, 'show_restaurants.html', {
        'restaurantList': restaurantList
    })


def delete_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    restaurant.delete()

    restaurantList = Restaurant.objects.all()
    return render(request, 'show_restaurants.html',{"restaurantList" : restaurantList})

def open_update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    itemList = restaurant.items.all()
    #itemList = Item.objects.all()
    return render(request, 'update_menu.html',{"itemList" : itemList, "restaurant" : restaurant})

def update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        vegeterian = request.POST.get('vegeterian') == 'on'
        picture = request.POST.get('picture')
        
        try:
            Item.objects.get(name = name)
            return HttpResponse("Duplicate item!")
        except:
            Item.objects.create(
                restaurant = restaurant,
                name = name,
                description = description,
                price = price,
                vegeterian = vegeterian,
                picture = picture,
            )
    return render(request, 'admin_home.html')

def view_menu(request, restaurant_id, username):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    itemList = restaurant.items.all()

    return render(
        request,
        'customer_menu.html',
        {
            "itemList": itemList,
            "restaurant": restaurant,
            "username": username
        }
    )
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, item_id, username):
    customer = request.user
    item = get_object_or_404(Item, id=item_id)

    cart, _ = Cart.objects.get_or_create(customer=customer)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        item=item
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("show_cart", username=customer.username)










@login_required
def show_cart(request, username):
    customer = request.user
    cart = Cart.objects.filter(customer=customer).first()

    cartItems = CartItem.objects.filter(cart=cart) if cart else []
    total = sum(ci.subtotal() for ci in cartItems)

    return render(request, "cart.html", {
        "cartItems": cartItems,
        "total": total,
        "username": customer.username
    })







import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import User, Cart

def checkout(request, username):
    customer = get_object_or_404(User, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    cart_items = cart.cart_items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    if total_price == 0:
        return render(request, 'checkout.html', {
            'username': username,
            'error': 'Your cart is empty!'
        })

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    order = client.order.create({
        "amount": int(total_price * 100),
        "currency": "INR",
        "payment_capture": 1
    })

    return render(request, 'checkout.html', {
        'username': username,
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': order['id'],
        'amount': total_price
    })






def orders(request, username):
    customer = get_object_or_404(User, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    cart_items = []
    total_price = 0

    if cart:
        cart_items = list(cart.cart_items.all())  # ✅ correct relation
        total_price = sum(ci.subtotal() for ci in cart_items)

        # clear cart
      

    return render(request, 'orders.html', {
        'username': username,
        'customer': customer,
        'cart_items': cart_items,
        'total_price': total_price,
    })


def remove_from_cart(request, item_id, username):
    customer = User.objects.get(username=username)
    cart = Cart.objects.get(customer=customer)

    item = Item.objects.get(id=item_id)
    cart.items.remove(item)

    return redirect('show_cart', username=username)



def increase_qty(request, cartitem_id, username):
    cart_item = get_object_or_404(CartItem, id=cartitem_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('show_cart', username=username)


def decrease_qty(request, cartitem_id, username):
    cart_item = get_object_or_404(CartItem, id=cartitem_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('show_cart', username=username)
from django.shortcuts import get_object_or_404, render, redirect
from .models import User, Cart

from django.http import JsonResponse
import json
import razorpay

from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Cart

@login_required
def place_order(request, username):
    customer = get_object_or_404(User, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    if not cart or not cart.cart_items.exists():
        return redirect("checkout", username=username)

    cart_items = list(cart.cart_items.all())
    total_price = cart.total_price()

    # clear cart
    cart.cart_items.all().delete()
    cart.delete()

    return render(request, "order_success.html", {
        "username": username,
        "cart_items": cart_items,
        "total_price": total_price,
    })






def ordersuccess(request, username):
    return render(request, 'order_success.html', {
        'username': username,
        'order_items': request.session.get('order_items', []),
        'total_price': request.session.get('order_total', 0),
    })






