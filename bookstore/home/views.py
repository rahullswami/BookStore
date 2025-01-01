from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *

@login_required(login_url='/accounts/login/')
def home(request):
    products = Product.objects.all()
    if request.GET.get('search'):
        search = request.GET.get('search')
        products = Product.objects.filter(
        Q(name__icontains = search)|
        Q(author__icontains = search)
        )
    return render(request, 'home.html', {'products':products})


@login_required(login_url='/accounts/login/')
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_details.html', {'product': product})



@login_required(login_url='/accounts/login/')
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = sum(item.total_price() for item in items)
    return render(request, 'cart.html', {'cart': cart, 'items': items, 'total': total})

@login_required(login_url='/accounts/login/')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required(login_url='/accounts/login/')
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart')

@login_required(login_url='/accounts/login/')
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity:
            cart_item.quantity = int(quantity)
            cart_item.save()
    return redirect('cart')

@login_required(login_url='/accounts/login/')
def checkout_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    if request.method == 'POST':
        order = Order.objects.create(user=request.user)
        for item in items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        cart.items.all().delete()  # Clear the cart
        return redirect('order_history')
    total = sum(item.total_price() for item in items)
    return render(request, 'checkout.html', {'cart': cart, 'items': items, 'total': total})

@login_required(login_url='/accounts/login/')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

@login_required(login_url='/accounts/login/')
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        order.delete()
        return redirect('order_history')
    return render(request, 'confirm_delete.html', {'order': order})
