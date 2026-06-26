import os
import django
from PIL import Image, ImageDraw, ImageFont

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafe.settings')
django.setup()

from coffee.models import Coffee
from django.core.files.base import ContentFile
from io import BytesIO

# Coffee colors for different types
COFFEE_COLORS = {
    'Espresso': '#2C1810',
    'Cappuccino': '#8B6F47',
    'Latte': '#D2B48C',
    'Americano': '#3E2723',
    'Mocha': '#6F4E37',
    'Black Coffee': '#1A1410',
    'Turkish Coffee': '#2C1810',
    'Affogato': '#F5DEB3',
    'Macchiato': '#A0826D',
    'Irish Coffee': '#8B4513',
    'Cold Brew': '#1C0F08',
    'Frappuccino': '#87CEEB',
    'Others': '#8B7355',
}

def generate_placeholder_image(category, name):
    """Generate a placeholder image for a coffee item"""
    # Create a new image with coffee-themed color
    color = COFFEE_COLORS.get(category, '#8B7355')
    # Convert hex to RGB
    color_rgb = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    
    img = Image.new('RGB', (300, 300), color_rgb)
    draw = ImageDraw.Draw(img)
    
    # Add a lighter gradient effect
    for y in range(150, 300):
        ratio = (y - 150) / 150
        r = int(color_rgb[0] * (1 - ratio * 0.3))
        g = int(color_rgb[1] * (1 - ratio * 0.3))
        b = int(color_rgb[2] * (1 - ratio * 0.3))
        draw.line([(0, y), (300, y)], fill=(r, g, b))
    
    # Add text
    try:
        # Try to use a system font, fall back to default if not available
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Draw coffee cup outline
    draw.rectangle([50, 30, 250, 180], outline='white', width=3)
    draw.arc([240, 160, 270, 200], 0, 360, fill='white', width=3)
    
    # Add coffee name
    text = name.replace(' ', '\n')
    draw.text((150, 220), text, fill='white', font=font, anchor='mm', align='center')
    
    return img

# Update each coffee with a placeholder image
coffees = Coffee.objects.all()
print(f"Generating images for {coffees.count()} coffee items...\n")

for coffee in coffees:
    print(f"Processing: {coffee.name}")
    
    # Generate placeholder image
    img = generate_placeholder_image(coffee.category, coffee.name)
    
    # Convert to bytes
    img_io = BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    
    # Create filename
    filename = f"{coffee.name.lower().replace(' ', '_')}.png"
    
    # Save to model
    coffee.image.save(filename, ContentFile(img_io.read()), save=True)
    print(f"  ✓ Image saved: {filename}\n")

print("✓ All coffee items now have placeholder images!")
