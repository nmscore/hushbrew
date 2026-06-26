import os
import django
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafe.settings')
django.setup()

from coffee.models import Coffee
from django.core.files.base import ContentFile
from io import BytesIO

# Create realistic coffee cup images
def create_coffee_image(name, category, temperature):
    """Create a realistic-looking coffee image"""
    
    # Different coffee colors
    colors = {
        'Espresso': {'bg': (139, 69, 19), 'coffee': (45, 24, 16), 'cup': (240, 240, 240)},
        'Cappuccino': {'bg': (210, 180, 140), 'coffee': (160, 82, 45), 'cup': (245, 245, 245)},
        'Latte': {'bg': (230, 190, 150), 'coffee': (205, 133, 63), 'cup': (250, 250, 250)},
        'Americano': {'bg': (120, 60, 30), 'coffee': (30, 20, 10), 'cup': (240, 240, 240)},
        'Mocha': {'bg': (139, 90, 43), 'coffee': (75, 45, 20), 'cup': (245, 245, 245)},
        'Black Coffee': {'bg': (50, 30, 15), 'coffee': (20, 10, 5), 'cup': (240, 240, 240)},
        'Turkish Coffee': {'bg': (101, 50, 18), 'coffee': (40, 20, 10), 'cup': (200, 200, 200)},
        'Affogato': {'bg': (245, 222, 179), 'coffee': (160, 82, 45), 'cup': (255, 250, 240)},
        'Macchiato': {'bg': (188, 143, 143), 'coffee': (100, 60, 30), 'cup': (245, 245, 245)},
        'Irish Coffee': {'bg': (139, 69, 19), 'coffee': (45, 24, 16), 'cup': (240, 240, 240)},
        'Cold Brew': {'bg': (40, 20, 10), 'coffee': (20, 10, 5), 'cup': (240, 240, 240)},
        'Frappuccino': {'bg': (135, 206, 235), 'coffee': (100, 50, 20), 'cup': (255, 255, 255)},
        'Others': {'bg': (160, 130, 100), 'coffee': (80, 50, 30), 'cup': (240, 240, 240)},
    }
    
    color_set = colors.get(category, colors['Others'])
    
    # Create image
    img = Image.new('RGB', (500, 500), color_set['bg'])
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Add gradient background
    for y in range(500):
        ratio = y / 500
        r = int(color_set['bg'][0] * (0.7 + ratio * 0.3))
        g = int(color_set['bg'][1] * (0.7 + ratio * 0.3))
        b = int(color_set['bg'][2] * (0.7 + ratio * 0.3))
        draw.line([(0, y), (500, y)], fill=(r, g, b))
    
    # Draw coffee cup
    cup_x, cup_y = 150, 120
    cup_w, cup_h = 200, 180
    
    # Cup body
    draw.ellipse([cup_x, cup_y, cup_x + cup_w, cup_y + 40], fill=color_set['cup'], outline='#888', width=2)
    draw.rectangle([cup_x, cup_y + 20, cup_x + cup_w, cup_y + cup_h], fill=color_set['cup'], outline='#888', width=2)
    draw.ellipse([cup_x, cup_y + cup_h - 20, cup_x + cup_w, cup_y + cup_h], fill=color_set['cup'], outline='#888', width=2)
    
    # Coffee inside cup
    coffee_top = cup_y + 30
    if temperature == 'Hot':
        coffee_color = color_set['coffee']
        # Add some steam effect
        draw.ellipse([cup_x + 40, coffee_top - 30, cup_x + 60, coffee_top - 10], fill=(*color_set['cup'], 80))
        draw.ellipse([cup_x + cup_w - 60, coffee_top - 25, cup_x + cup_w - 40, coffee_top - 5], fill=(*color_set['cup'], 100))
        # Foam
        draw.ellipse([cup_x + 20, coffee_top - 5, cup_x + cup_w - 20, coffee_top + 15], fill=(255, 250, 240, 200))
    else:
        # Cold drink with ice
        coffee_color = (*color_set['coffee'][:3], 230)
        # Ice cubes
        draw.rectangle([cup_x + 30, coffee_top + 40, cup_x + 70, coffee_top + 80], fill=(200, 220, 255), outline=(180, 200, 240), width=1)
        draw.rectangle([cup_x + 80, coffee_top + 30, cup_x + 120, coffee_top + 70], fill=(200, 220, 255), outline=(180, 200, 240), width=1)
    
    # Coffee liquid
    draw.rectangle([cup_x + 5, coffee_top, cup_x + cup_w - 5, cup_y + cup_h - 30], fill=coffee_color)
    
    # Handle
    handle_x = cup_x + cup_w + 10
    handle_y = cup_y + 50
    draw.arc([handle_x, handle_y, handle_x + 50, handle_y + 80], 0, 360, fill='#888', width=3)
    
    # Add saucer
    draw.ellipse([cup_x - 40, cup_y + cup_h - 10, cup_x + cup_w + 40, cup_y + cup_h + 20], fill=color_set['cup'], outline='#999', width=2)
    
    # Add text
    try:
        font_name = ImageFont.truetype("arial.ttf", 36)
        font_small = ImageFont.truetype("arial.ttf", 20)
    except:
        font_name = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Coffee name
    text_y = cup_y + cup_h + 60
    draw.text((250, text_y), name, fill=(240, 240, 240), font=font_name, anchor='mm')
    
    # Category and temperature
    draw.text((250, text_y + 50), f"{category} - {temperature}", fill=(200, 200, 200), font=font_small, anchor='mm')
    
    return img

print("Creating professional-looking coffee images...\n")

coffees = Coffee.objects.all()

for coffee in coffees:
    print(f"Creating: {coffee.name}")
    
    try:
        # Create image
        img = create_coffee_image(coffee.name, coffee.category, coffee.temperature)
        
        # Delete old image
        if coffee.image:
            coffee.image.delete()
        
        # Save to buffer
        img_io = BytesIO()
        img.save(img_io, format='JPEG', quality=95)
        img_io.seek(0)
        
        # Save to model
        filename = f"{coffee.name.lower().replace(' ', '_')}.jpg"
        coffee.image.save(filename, ContentFile(img_io.read()), save=True)
        print(f"  ✓ Created: {filename}\n")
        
    except Exception as e:
        print(f"  ✗ Error: {str(e)[:50]}\n")

print("✓ All coffee images created successfully!")
