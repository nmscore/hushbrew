import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafe.settings')
django.setup()

from coffee.models import Coffee
from django.core.files.base import ContentFile

# Stable real coffee photo URLs from Unsplash
COFFEE_IMAGES = {
    'Espresso Shot': 'https://images.unsplash.com/photo-1511920170033-f8396924c348?auto=format&fit=crop&w=1000&q=80',
    'Cappuccino Classic': 'https://images.unsplash.com/photo-1506619216599-9d16d0903dfd?auto=format&fit=crop&w=1000&q=80',
    'Latte Vanilla': 'https://images.unsplash.com/photo-1610632380989-680fe40816c6?auto=format&fit=crop&w=1000&q=80',
    'Americano Bold': 'https://images.unsplash.com/photo-1541167760496-1628856ab772?auto=format&fit=crop&w=1000&q=80',
    'Mocha Deluxe': 'https://images.unsplash.com/photo-1559496417-e7f25cb247f3?auto=format&fit=crop&w=1000&q=80',
    'Iced Latte': 'https://images.unsplash.com/photo-1542372147193-a7aca54189cd?auto=format&fit=crop&w=1000&q=80',
    'Cold Brew': 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=1000&q=80',
    'Frappuccino Berry': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=1000&q=80',
    'Turkish Coffee': 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?auto=format&fit=crop&w=1000&q=80',
    'Macchiato Perfetto': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1000&q=80',
    'Black Coffee Premium': 'https://images.unsplash.com/photo-1512568400610-62da28bc8a13?auto=format&fit=crop&w=1000&q=80',
    'Affogato Dream': 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=1000&q=80',
}

print('Downloading real coffee images from Unsplash...\n')

coffees = Coffee.objects.all()
success = 0

for coffee in coffees:
    print(f'Processing: {coffee.name}')
    
    if coffee.name in COFFEE_IMAGES:
        try:
            url = COFFEE_IMAGES[coffee.name]
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0'
            }
            
            print('  Downloading from Unsplash...')
            response = requests.get(url, timeout=20, headers=headers)
            response.raise_for_status()
            
            if coffee.image:
                coffee.image.delete(save=False)
            
            filename = f"{coffee.name.lower().replace(' ', '_')}.jpg"
            coffee.image.save(filename, ContentFile(response.content), save=True)
            print(f'  ✓ Image saved: {filename}\n')
            success += 1
            
        except Exception as e:
            print(f'  ✗ Error: {str(e)[:100]}\n')

print(f'\n✓ Successfully downloaded {success} out of {len(coffees)} coffee images!')
