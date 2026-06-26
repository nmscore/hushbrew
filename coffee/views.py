from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Coffee, CartItem
from .forms import CoffeeForm, CustomRegisterForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

from .models import CartItem



def home(request):
    coffee = Coffee.objects.all()

    category = request.GET.get('category', '').strip()
    temperature = request.GET.get('temperature', '').strip()

    if category:
        coffee = coffee.filter(category__iexact=category)

    if temperature:
        coffee = coffee.filter(temperature__iexact=temperature)

    search_query = request.GET.get('search', '').strip()
    if search_query:
        coffee = coffee.filter(name__icontains=search_query)

    categories = Coffee.CATEGORY_CHOICES
    return render(request, 'home.html', {
        'coffee': coffee,
        'categories': categories,
        'search_query': search_query,
    })


def add_coffee(request):
    if request.method == 'POST':
        form = CoffeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CoffeeForm()
    return render(request, 'shop/coffee_form.html', {'form': form})


def add_to_cart(request, coffee_id):
    coffee = get_object_or_404(Coffee, id=coffee_id)

    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    cart_item, created = CartItem.objects.get_or_create(
        product=coffee,
        session_key=session_key,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


def cart_view(request):
    if not request.session.session_key:
        request.session.create() 
   
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)
    total_price = sum(item.subtotal() for item in cart_items)

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


@require_POST
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, session_key=request.session.session_key)
    new_quantity = int(request.POST.get('quantity', 1))
    cart_item.quantity = max(1, new_quantity)
    cart_item.save()
    return redirect('cart')


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, session_key=request.session.session_key)
    cart_item.delete()
    return redirect('cart')


def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome")
            return redirect('home')  # Redirect to coffee home
        else:
            messages.error(request, "Already registered user credentials!")
    else:
        form = CustomRegisterForm()
    return render(request, 'shop/register.html', {'form': form})


def custom_logout(request):
    logout(request)
    return render(request, 'goodbye.html')  # Shows thank you message


def cover_page(request):
    coffee = Coffee.objects.all()
    return render(request, 'cover.html', {'coffee': coffee})

@login_required(login_url='login')
def checkout(request):

    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)
    total_price = sum(item.subtotal() for item in cart_items)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')

    return render(request, 'shop/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


@require_POST
def confirm_order(request):
    if not request.user.is_authenticated:
        return redirect('login')

    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_items = CartItem.objects.filter(session_key=session_key)

    if not cart_items.exists():
        messages.warning(request, "Cart is empty.")
        return redirect('cart')

    total_price = sum(item.subtotal() for item in cart_items)

    # ✅ Create the order with required fields
    order = Order.objects.create(
        user=request.user,
        total_price=total_price,
        # email is optional here if removed from model
    )

    # ✅ Add items to the order
    for item in cart_items:
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

    cart_items.delete()

    # ✅ Redirect to thank you page with order ID
    return redirect('thank_you', order_id=order.id)


def thank_you(request, order_id):
    if not request.user.is_authenticated:
        return redirect('login')

    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/thank_you.html', {'order': order})

def about_view(request):
        return render(request, 'about.html')

#def menu_view(request):
        #coffee = Coffee.objects.all()
        #return render(request, 'shop/menu.html',{'coffee': coffee})        




def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # Save the old session key (before login)
            old_session_key = request.session.session_key

            # Login the user
            auth_login(request, user)

            # Ensure session is saved and new key is available
            request.session.save()
            new_session_key = request.session.session_key

            # Transfer cart items from old session to new session
            if old_session_key and new_session_key and old_session_key != new_session_key:
                CartItem.objects.filter(session_key=old_session_key).update(session_key=new_session_key)

            return redirect('checkout')  # Or 'home' if you prefer
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})



from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Order

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/order_history.html', {'orders': orders})



from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        new_password = request.POST.get('new_password1')

        # Custom validation: new password must not contain username
        if request.user.username.lower() in new_password.lower():
            form.add_error('new_password1', 'New password cannot contain your username.')
        elif form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password is now changed')
            return redirect('change_password')

    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'shop/change_password.html', {'form': form})

def forgot_password(request):
    return render(request, 'shop/forgot_password.html')



# ✅ Context processor to count cart items for current session
def cart_item_count(request):
    cart_count = 0
    if request.session.session_key:
        cart_count = CartItem.objects.filter(session_key=request.session.session_key).count()
    return {'cart_count': cart_count}







