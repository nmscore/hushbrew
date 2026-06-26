from django.db import models
from django.contrib.auth.models import User

class Coffee(models.Model):
    CATEGORY_CHOICES= [
        ('Cappuccino', 'Cappuccino'),
        ('Latte', 'Latte'),
        ('Black Coffee', 'Black Coffee'),
        ('Americano', 'Americano'),
        ('Mocha', 'Mocha'),
        ('Espresso', 'Espresso'),
        ('Turkish Coffee', 'Turkish Coffee'),
        ('Affogato', 'Affogato'),
        ('Macchiato', 'Macchiato'),
        ('Irish Coffee', 'Irish Coffee'),
        ('Cold Brew', 'Cold Brew'),
        ('Frappuccino', 'Frappuccino'),
        ('Others', 'Others'),
    ]

    TEMPERATURE_CHOICES = [
        ('Hot', 'Hot'),
        ('Cold', 'Cold'),
    ]

    name = models.CharField(max_length=255)
    price = models.FloatField()
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Others')
    temperature = models.CharField(max_length=10, choices=TEMPERATURE_CHOICES, default='Hot')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    product = models.ForeignKey(Coffee, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    session_key = models.CharField(max_length=100)

    def subtotal(self):
        return self.quantity * self.product.price


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Coffee', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def subtotal(self):
        return round(self.product.price * self.quantity, 2)



