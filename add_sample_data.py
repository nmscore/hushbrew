import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafe.settings')
django.setup()

from coffee.models import Coffee

# Sample coffee items
sample_coffees = [
    {
        'name': 'Espresso Shot',
        'price': 2.50,
        'quantity': 100,
        'category': 'Espresso',
        'temperature': 'Hot',
        'description': 'Single shot of rich, concentrated espresso.',
    },
    {
        'name': 'Cappuccino Classic',
        'price': 4.50,
        'quantity': 80,
        'category': 'Cappuccino',
        'temperature': 'Hot',
        'description': 'Smooth cappuccino with velvety steamed milk.',
    },
    {
        'name': 'Latte Vanilla',
        'price': 4.75,
        'quantity': 75,
        'category': 'Latte',
        'temperature': 'Hot',
        'description': 'Creamy latte with a hint of vanilla flavor.',
    },
    {
        'name': 'Americano Bold',
        'price': 3.50,
        'quantity': 90,
        'category': 'Americano',
        'temperature': 'Hot',
        'description': 'Strong Americano with hot water and espresso.',
    },
    {
        'name': 'Mocha Deluxe',
        'price': 5.00,
        'quantity': 70,
        'category': 'Mocha',
        'temperature': 'Hot',
        'description': 'Rich mocha with espresso and chocolate.',
    },
    {
        'name': 'Iced Latte',
        'price': 4.75,
        'quantity': 85,
        'category': 'Latte',
        'temperature': 'Cold',
        'description': 'Refreshing iced latte perfect for summer days.',
    },
    {
        'name': 'Cold Brew',
        'price': 4.00,
        'quantity': 95,
        'category': 'Cold Brew',
        'temperature': 'Cold',
        'description': 'Smooth and mellow cold brew coffee.',
    },
    {
        'name': 'Frappuccino Berry',
        'price': 5.25,
        'quantity': 60,
        'category': 'Frappuccino',
        'temperature': 'Cold',
        'description': 'Blended frappuccino with mixed berries.',
    },
    {
        'name': 'Turkish Coffee',
        'price': 3.75,
        'quantity': 50,
        'category': 'Turkish Coffee',
        'temperature': 'Hot',
        'description': 'Traditional Turkish coffee prepared in a cezve.',
    },
    {
        'name': 'Macchiato Perfetto',
        'price': 4.25,
        'quantity': 65,
        'category': 'Macchiato',
        'temperature': 'Hot',
        'description': 'Espresso marked with a dollop of steamed milk.',
    },
    {
        'name': 'Black Coffee Premium',
        'price': 3.00,
        'quantity': 110,
        'category': 'Black Coffee',
        'temperature': 'Hot',
        'description': 'Pure black coffee - nothing but perfection.',
    },
    {
        'name': 'Affogato Dream',
        'price': 5.50,
        'quantity': 40,
        'category': 'Affogato',
        'temperature': 'Hot',
        'description': 'Vanilla ice cream topped with hot espresso.',
    },
]

# Clear existing coffee items
Coffee.objects.all().delete()
print("✓ Cleared existing coffee items")

# Add new sample items
for coffee_data in sample_coffees:
    coffee = Coffee.objects.create(**coffee_data)
    print(f"✓ Added: {coffee.name}")

print(f"\n✓ Successfully added {len(sample_coffees)} coffee items!")
