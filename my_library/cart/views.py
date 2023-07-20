from django.shortcuts import render, redirect, get_object_or_404
from mylibrary.models import Book_details
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, id):
    book = Book_details.objects.get(id=id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()
    try:
        cart_item = CartItem.objects.get(book=book, cart=cart)
        if cart_item.quantity < cart_item.book.stock:
            cart_item.quantity += 1
            cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            book=book,
            quantity=1,
            cart=cart
        )
        cart_item.save()
    return redirect('cart:cart_details')


def cart_details(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.book.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter))


def cart_remove(request, book_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    book = get_object_or_404(Book_details, id=book_id)
    cart_item = CartItem.objects.get(book=book, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_details')


def full_remove(request, book_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    book = get_object_or_404(Book_details, id=book_id)
    cart_item = CartItem.objects.get(book=book, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_details')


def clear_cart(request):
    # Clear the cart items and set the amount to zero
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart)
    cart_items.delete()

    # Redirect back to the cart details page
    return redirect('cart:cart_details')
