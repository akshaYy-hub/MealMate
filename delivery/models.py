from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    username = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)
    email = models.CharField(max_length = 20)
    mobile = models.CharField(max_length = 10)
    address = models.CharField(max_length = 50)

    def __str__(self):
        return self.username
    
class Restaurant(models.Model):
    name = models.CharField(max_length = 20)
    picture = models.URLField(max_length = 200, default='https://m.ahstatic.com/is/image/accorhotels/HCM_P_8147067:4by3?fmt=jpg&op_usm=1.75,0.3,2,0&resMode=sharp2&iccEmbed=true&icc=sRGB&dpr=on,1.5&wid=335&hei=251&qlt=80')
    cuisine = models.CharField(max_length = 200)
    rating = models.FloatField()

class Item(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE, related_name = "items")
    name = models.CharField(max_length = 20)
    description = models.CharField(max_length = 200)
    price = models.FloatField()
    vegeterian = models.BooleanField(default=False)
    picture = models.URLField(max_length = 400, default='https://www.indiafilings.com/learn/wp-content/uploads/2024/08/How-to-Start-Food-Business.jpg')
from django.contrib.auth.models import User



class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def total_price(self):
        return sum(ci.subtotal() for ci in self.cart_items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, related_name="cart_items", on_delete=models.CASCADE
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.item.price * self.quantity

     
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    status = models.CharField(max_length=20, default="PLACED")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()


    