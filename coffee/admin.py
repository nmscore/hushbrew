from django.contrib import admin
from . models import Coffee

@admin.register(Coffee)
class CoffeeAdmin(admin.ModelAdmin):
    list_display = ('name' , 'price' , 'quantity', 'category', 'temperature')
    fields = ['name', 'price', 'quantity', 'description', 'image', 'category', 'temperature']
    