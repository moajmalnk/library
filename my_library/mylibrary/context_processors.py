from cart.models import Cart, CartItem
from cart.views import _cart_id
from mylibrary.models import *
from django.db.models import Sum


def book_links(request):
    books = Book_details.objects.all().order_by("-id")[:5]
    lang = Language.objects.all().order_by('id')
    lang_count = lang.count()
    news = Newspaper.objects.all().order_by('id')
    news_count = news.count()
    message = Notifications.objects.all()
    message_count = message.count()
    cbook = Book_details.objects.all().order_by('-id')
    book_count = cbook.count()
    patron = Patron.objects.all()
    patron_count = patron.count()
    patron_percentage = patron_count * 100 / 100
    links = Category.objects.all().order_by("id")
    category_count = links.count()
    i_book = list(IssuedBook.objects.all()) + list(Book_details.objects.all())
    t_issued_books = IssuedBook.objects.filter(returned=False).order_by('-id')
    t_issued_books_count = t_issued_books.count()
    t_returned_books = IssuedBook.objects.filter(returned=True).order_by('-id')
    t_returned_books_count = t_returned_books.count()
    notify = Notifications.objects.all()
    notify_count = notify.count()
    cart = CartItem.objects.all().order_by('-id')
    cart_count = cart.count()
    return {
        'issued_books': t_issued_books,
        'notify_count': notify_count,
        't_returned_books_count': t_returned_books_count,
        't_issued_books_count': t_issued_books_count,
        'nav_books': books,
        'lang': lang,
        'links': links,
        'i_book': i_book,
        'news': news,
        'news_count': news_count,
        'cbook': cbook,
        'message_count': message_count,
        'message': message,
        'book_count': book_count,
        'patron': patron,
        'patron_count': patron_count,
        'patron_percentage': patron_percentage,
        'category_count': category_count,
        'lang_count': lang_count,
        'cart_count': cart_count
    }


def counter(request):
    item_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart[:1])
            for cart_item in cart_items:
                item_count += cart_item.quantity
        except Cart.DoesNotExist:
            item_count = 0
    return dict(item_count=item_count)


def total_all_patrons_fine(self):
    total_fines = Patron.objects.aggregate(total_fine=Sum('fine'))['total_fine'] or 0
    patrons = Patron.objects.all()
    total_patron_fine = 0
    for patron in patrons:
        total_patron_fine += patron.paid + patron.fine
    percentage_fine = total_patron_fine * 10 / 2500
    return {
        'total_fines': total_fines,
        'total_patron_fine': total_patron_fine,
        'percentage_fine': percentage_fine
        }


def menu_links(request):
    patrons = Patron.objects.all().order_by('-id')

    # Initialize variables to hold the main patron and other patrons
    main_patron = None
    other_patrons = []

    if request.user.is_authenticated:
        user_email = request.user.email

        # Loop through the patrons and categorize them
        for patron in patrons:
            if patron.gmail == user_email:
                main_patron = patron
            else:
                other_patrons.append(patron)

    # If the main patron is found, insert it at the beginning of the list
    if main_patron:
        other_patrons.insert(0, main_patron)
    other_patrons = other_patrons[:5]

    return {
        'navbar_patrons': other_patrons,
        'patrons': patrons,
    }
