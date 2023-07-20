import datetime
import re
import tempfile
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from cart.models import *
from .forms import *
from .models import *


# updates
def update_book(request, id):
    book = get_object_or_404(Book_details, id=id)
    form = BookForm(request.POST or None, instance=book)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            book_detail_url = reverse('mylibrary:detail', args=[book.id])
            return redirect(book_detail_url)

    book_detail_url = reverse('mylibrary:detail', args=[book.id])
    context = {
        'u_book': book,
        'form': form,
        'book_detail_url': book_detail_url
    }
    template = 'update.html'
    return render(request, template, context)


def update_patron(request, id):
    patron = get_object_or_404(Patron, id=id)
    form = PatronForm(request.POST or None, instance=patron)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            patron_detail_url = reverse('search_app:profile', args=[patron.id])
            return redirect(patron_detail_url)
    patron_detail_url = reverse('search_app:profile', args=[patron.id])
    context = {
        'u_patron': patron,
        'form': form,
        'patron_detail_url': patron_detail_url
    }
    template = 'update.html'
    return render(request, template, context)


def update_notify(request, id):
    notify = get_object_or_404(Notifications, id=id)
    form = NotificationsForm(request.POST or None, instance=notify)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            notify_detail_url = reverse('mylibrary:program', args=[notify.id])
            return redirect(notify_detail_url)
    notify_detail_url = reverse('mylibrary:program', args=[notify.id])
    context = {
        'u_notify': notify,
        'form': form,
        'notify_detail_url': notify_detail_url
    }
    return render(request, 'update.html', context)


def update_news(request, id):
    news = get_object_or_404(Newspaper, id=id)
    form = NewsForm(request.POST or None, instance=news)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            news_detail_url = reverse('mylibrary:newspaper')
            return redirect(news_detail_url)
    news_detail_url = reverse('mylibrary:newspaper')
    context = {
        'u_news': news,
        'form': form,
        'news_detail_url': news_detail_url
    }
    return render(request, 'update.html', context)


# delete items
def delete_category(request, id):
    cat = Category.objects.get(id=id)
    if request.method == 'POST':
        category = Category.objects.get(id=id)
        category.delete()
        return redirect('mylibrary:home')
    context = {
        'category': cat
    }
    template = "delete.html"
    return render(request, template, context)


def delete_newspaper(request, id):
    news = Newspaper.objects.get(id=id)
    if request.method == 'POST':
        newspaper = Newspaper.objects.get(id=id)
        newspaper.delete()
        return redirect('/mylibrary/newspaper/')
    context = {
        'newspaper': news
    }
    template = "delete.html"
    return render(request, template, context)


def delete_book(request, id):
    book = Book_details.objects.get(id=id)
    if request.method == 'POST':
        book = Book_details.objects.get(id=id)
        book.delete()
        return redirect('/mylibrary/')
    context = {
        'book': book
    }
    return render(request, 'delete.html', context)


def delete_notify(request, id):
    notify = Notifications.objects.get(id=id)
    if request.method == 'POST':
        notify = Notifications.objects.get(id=id)
        notify.delete()
        return redirect('/mylibrary/')
    context = {
        'notify': notify
    }
    return render(request, 'delete.html', context)


def delete_patron(request, id):
    patron = Patron.objects.get(id=id)
    if request.method == 'POST':
        patron = Patron.objects.get(id=id)
        patron.delete()
        return redirect('/mylibrary/all_patrons/')
    context = {
        'patron': patron
    }
    template = 'delete.html'
    return render(request, template, context)


# add items
def add_book(request):
    last_primary_number = Book_details.objects.order_by('-primary_number').first()
    if last_primary_number:
        next_primary_number = int(last_primary_number.primary_number) + 1
    else:
        next_primary_number = 991001
    if request.method == 'POST':
        primary_number = request.POST.get('primary_number')
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        desc = request.POST.get('desc')
        author = request.POST.get('author')
        category_name = request.POST.get('category')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        # img = request.FILES['img']
        pdf = request.FILES['pdf']
        lang_name = request.POST.get('lang')
        category = Category.objects.get(name=category_name)
        lang = Language.objects.get(name=lang_name)
        if Book_details.objects.filter(primary_number=primary_number).exists():
            messages.info(request, "Book number already exists")
            return redirect('mylibrary:add_book')
        elif Book_details.objects.filter(slug=slug).exists():
            messages.info(request, "Book Name already exists")
            return redirect('mylibrary:add_book')
        else:
            book = Book_details(
                primary_number=primary_number, name=name,
                slug=slug, desc=desc, author=author, category=category,
                price=price, stock=stock, pdf=pdf, lang=lang
            )
            book.save()
            return redirect('mylibrary:add_book')
    book = Book_details.objects.all()
    context = {
        'book': book,
        'next_primary_number': next_primary_number,
    }
    return render(request, 'add.html', context)


def add_newspaper(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        pdf = request.FILES['pdf']
        if name:
            if not re.match(r'^[A-Za-z\s]+$', name):
                messages.warning(request, "News Paper name should only contain alphabetic characters.")
                return redirect('search_app:add_newspaper')
            if Category.objects.filter(slug=slug).exists():
                messages.info(request, 'Newspaper Already Exists')
                return redirect('search_app:add_newspaper')
            else:
                newspaper = Newspaper(name=name, slug=slug, pdf=pdf)
                newspaper.save()
                messages.info(request, f'The {name} Newspaper successfully added')
        else:
            messages.warning(request, "Please enter a valid name.")
    newspaper = Newspaper.objects.all()
    context = {
        'newspaper': newspaper
    }
    template = 'add.html'
    return render(request, template, context)


def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        if name:
            if not re.match(r'^[A-Za-z\s]+$', name):
                messages.warning(request, "Category name should only contain alphabetic characters.")
                return redirect('search_app:add_category')
            if Category.objects.filter(slug=slug).exists():
                messages.info(request, 'CATEGORY EXISTS')
                return redirect('search_app:add_category')
            else:
                category = Category(name=name, slug=slug)
                category.save()
                messages.info(request, f'The {name} Category successfully added')
        else:
            messages.warning(request, "Please enter a valid name.")
    category = Category.objects.all()
    context = {
        'category': category
    }
    template = 'add.html'
    return render(request, template, context)


def add_patrons(request):
    last_card_no = Patron.objects.order_by('-card_no').first()
    if last_card_no:
        next_card_no = int(last_card_no.card_no) + 1
    else:
        next_card_no = 10091
    if request.method == 'POST':
        name = request.POST.get('name')
        gmail = request.POST.get('gmail')
        card_no = request.POST.get('card_no')
        phone = request.POST.get('phone')
        # img = request.FILES['img']
        if Patron.objects.filter(card_no=card_no).exists():
            messages.info(request, "Card number already exists")
            return redirect('mylibrary:add_patron')
        elif Patron.objects.filter(name=name).exists():
            messages.info(request, "Name already exists")
            return redirect('mylibrary:add_patron')
        elif Patron.objects.filter(gmail=gmail).exists():
            messages.info(request, "Mail already exists")
            return redirect('mylibrary:add_patron')
        else:
            patron = Patron(name=name, gmail=gmail, card_no=card_no, phone=phone)
            patron.save()
            return redirect('mylibrary:add_patron')
    patron = Patron.objects.all()
    context = {
        'card_id': next_card_no,
        'patron': patron
    }
    return render(request, 'add.html', context)


def add_notifications(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        on = request.POST.get('on')
        location = request.POST.get('location')
        inauguration = request.POST.get('inauguration')
        welcome_speech = request.POST.get('welcome_speech')
        presidential_speech = request.POST.get('presidential_speech')
        greetings = request.POST.get('greetings')
        special_speech = request.POST.get('special_speech')
        speech = request.POST.get('speech')
        song = request.POST.get('song')
        vote_of_thanks = request.POST.get('vote_of_thanks')
        if Notifications.objects.filter(name=name).exists():
            messages.info(request, 'programme already exists')
            return redirect('search_app:add_notify')
        else:
            notification = Notifications(
                name=name, on=on, location=location,
                inauguration=inauguration, welcome_speech=welcome_speech,
                presidential_speech=presidential_speech, greetings=greetings,
                special_speech=special_speech, speech=speech,
                song=song, vote_of_thanks=vote_of_thanks,
            )
            notification.save()
            return redirect('/library/add_notification/')
    notify = Notifications.objects.all()
    context = {
        'notify': notify
    }
    return render(request, 'add.html', context)


# user signup and login
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username is already taken')
            return redirect('mylibrary:signup')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email is Already Taken')
            return redirect('mylibrary:signup')
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
        return redirect('mylibrary:login')
    return render(request, 'signup.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/mylibrary/')
    if request.method == 'POST':
        username_or_email = request.POST['username_or_email']
        password = request.POST['password']
        if '@' in username_or_email:
            user = authenticate(request, email=username_or_email, password=password)
        else:
            user = authenticate(request, username=username_or_email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/mylibrary/')
        else:
            messages.error(request, 'Invalid credentials. Please try again. ')
            return redirect('/mylibrary/login/')
        return redirect("/mylibrary/")
    return render(request, 'login.html')


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/mylibrary/login/')


# patron details
def profile(request, id):
    patron = Patron.objects.get(id=id)
    context = {
        'patron': patron
    }
    template = 'profile.html'
    return render(request, template, context)


def all_patrons(request):
    patron = Patron.objects.all()
    template = 'all_patrons.html'
    context = {
        'patron': patron
    }
    return render(request, template, context)


# home page
def home(request, slug=None):
    if request.user.is_authenticated:
        if slug is not None:
            page = get_object_or_404(Book_details, slug=slug)
            book_list = Book_details.objects.all().filter(category=page).order_by('id')
        else:
            book_list = Book_details.objects.all().filter().order_by('id')
        paginator = Paginator(book_list, 8)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            books = paginator.page(page)
        except (EmptyPage, InvalidPage):
            books = paginator.page(paginator.num_pages)

        return render(request, 'home.html', {'book': books, 'category': page, 'paginator': paginator})
    return redirect('/mylibrary/')


# books detail view
def detail_view(request, id):
    book = Book_details.objects.get(id=id)
    book.increment_download()
    context = {
        'book': book
    }
    return render(request, 'detail.html', context)


def programmes(request, id):
    msg = Notifications.objects.get(id=id)
    context = {
        'msg': msg
    }
    return render(request, 'programmes.html', context)


def all_programmes(request):
    msg = Notifications.objects.all().order_by('-id')
    context = {
        'all_msg': msg
    }
    return render(request, 'programmes.html', context)


def download(request, id):
    msg = Notifications.objects.get(id=id)
    context = {
        'msg': msg
    }
    return render(request, 'download.html', context)


def all_book_category(request, c_slug=None):
    c_page = None

    if c_slug is not None:
        c_page = get_object_or_404(Category, slug=c_slug)
        books_list = Book_details.objects.filter(category=c_page, available=True).order_by('id')
    else:
        books_list = Book_details.objects.filter(available=True).order_by('id')
    context = {
        'category': c_page,
        'books': books_list,
    }
    template = 'category.html'
    return render(request, template, context)


def all_book_details(request, c_slug, book_slug):
    try:
        book = Book_details.objects.get(category__slug=c_slug, slug=book_slug)
    except Exception as e:
        raise e
    return render(request, 'detail.html', {'book': book})


def superuser(request):
    template = 'superuser.html'
    return render(request, template)


def news_paper(request):
    newspaper = Newspaper.objects.all().order_by('id')
    context = {
        'newspaper': newspaper
    }
    return render(request, 'news paper.html', context)


# generate pdf for download
def generate_pdf(html_content):
    result = tempfile.NamedTemporaryFile(delete=False)

    pdf = pisa.CreatePDF(html_content, dest=result)

    if not pdf.err:
        result.close()
        return result.name

    return None


def download_card(request, notification_id):
    notification = get_object_or_404(Notifications, id=notification_id)

    # Render the card template to HTML
    card_html = render_to_string('download.html', {'msg': notification}, request=request)

    # Create a PDF file using the card HTML
    pdf_path = generate_pdf(card_html)

    if pdf_path:
        # Read the PDF file content
        with open(pdf_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        # Create the HttpResponse with the PDF file
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="your_file.pdf"'

        return response

    return HttpResponse("Error generating PDF")


# issue return work in progress
def issue_patron(request, id):
    patron = get_object_or_404(Patron, id=id)
    issue_date = datetime.date.today()
    return_date = issue_date + datetime.timedelta(days=7)
    due_date = return_date + datetime.timedelta(days=1)
    due_book = Book_details.objects.all()
    issued_books = IssuedBook.objects.filter(patron=patron, returned=False).order_by('-id')
    max_issued_books = 3  # Maximum number of books a patron can issue
    current_issued_books = issued_books.count()

    if patron.fine > 0:
        messages.warning(request, "Please pay your pending fine to issue books.")
        return redirect('search_app:return_patron', id=patron.id)

    if request.method == 'POST':
        primary_number = request.POST.get('primary_number')
        book = get_object_or_404(Book_details, primary_number=primary_number)

        if book.is_issued:
            messages.info(request, f"The book '{book.name}' is already issued by '{book.issued_to.name}'.")
        else:
            if current_issued_books < max_issued_books:
                book.is_issued = True
                book.issued_to = patron
                book.save()

                issued_book = IssuedBook(book=book, patron=patron, issue_date=issue_date, return_date=return_date)
                issued_book.save()

                messages.success(request, f"The book '{book.name}' has been issued to '{patron.name}'.")
            else:
                messages.warning(request, "The patron has reached the maximum limit of 3 issued books.")

    context = {
        'patron': patron,
        'issued_books': issued_books,
        'due_date': due_date,
        'due_book': due_book,
        'current_issued_books': current_issued_books,
        'max_issued_books': max_issued_books
    }

    return render(request, 'issue_book.html', context)


def return_patron(request, id):
    patron = get_object_or_404(Patron, id=id)
    returned_books = IssuedBook.objects.filter(patron=patron, returned=False).order_by('-id')

    if request.method == 'POST':
        primary_number = request.POST.get('primary_number')
        book = get_object_or_404(Book_details, primary_number=primary_number)

        if not book.is_issued:
            messages.info(request, f"The book '{book.name}' is already returned.")
        else:
            issued_book = IssuedBook.objects.filter(returned=False, patron=patron).first()
            if issued_book:
                issued_book.returned = True
                issued_book.save()

                book = issued_book.book
                book.is_issued = False
                book.issued_to = None
                book.save()

                # Calculate the fine if the book is returned after the return date
                return_date = issued_book.return_date
                today = datetime.date.today()

                if today > return_date:
                    days_overdue = (today - return_date).days
                    fine = days_overdue * 20  # Assuming the fine amount is 20 rupees per day
                    issued_book.fine = fine
                    # Update the patron's fine amount
                    patron.fine = fine
                    patron.save()
                    issued_book.return_date = datetime.date.today()
                    issued_book.save()

                messages.success(request, f"The book '{book.name}' has been returned by '{patron.name}'.")

        return redirect('search_app:return_patron', id=id)

    context = {
        'patron': patron,
        'returned_books': returned_books
    }

    return render(request, 'return_book.html', context)


def renew_patron(request, id):
    issued_book = get_object_or_404(IssuedBook, id=id)
    patron = issued_book.patron
    book = issued_book.book

    if issued_book.renewal_count >= 2:
        messages.warning(request, f"The book '{book.name}' has reached the maximum number of renewals.")
        return redirect('search_app:issue_patron', id=patron.id)

    # Calculate the new return date by adding 7 days to the current return date
    new_return_date = issued_book.return_date + datetime.timedelta(days=7)

    # Update the return date and renewal count of the issued book
    issued_book.return_date = new_return_date
    issued_book.renewal_count += 1
    issued_book.save()

    # Reissue the book with a new issue date and set is_issued to True
    book.is_issued = True
    book.save()

    messages.success(request,
                     f"The book '{book.name}' has been renewed. The new return date is {new_return_date}. The book has been reissued.")

    return redirect('search_app:issue_patron', id=patron.id)


def renew_all_books(request, id):
    patron = get_object_or_404(Patron, id=id)
    issued_books = IssuedBook.objects.filter(patron=patron)
    for issued_book in issued_books:
        if issued_book.renewal_count < 2:
            issued_book.renewal_count += 1
            new_return_date = issued_book.return_date + datetime.timedelta(days=7)
            issued_book.return_date = new_return_date
            issued_book.save()

            issued_book.book.is_issued = True
            issued_book.book.issued_to = patron
            issued_book.book.save()
    messages.success(request, f"All books for {patron.name} have been renewed and The book has been reissued.")
    return redirect('search_app:issue_patron', id=patron.id)


def return_all_books(request, id):
    patron = get_object_or_404(Patron, id=id)
    issued_books = IssuedBook.objects.filter(patron=patron, returned=False).order_by('id')

    if issued_books:
        total_fine = 0

        for issued_book in issued_books:
            issued_book.returned = True
            issued_book.save()

            book = issued_book.book
            book.is_issued = False
            book.issued_to = None
            book.save()

            # Calculate the fine if the book is returned after the return date
            return_date = issued_book.return_date
            today = datetime.date.today()

            if today > return_date:
                days_overdue = (today - return_date).days
                fine = days_overdue * 20  # Assuming the fine amount is 20 rupees per day
                total_fine += fine

                issued_book.fine += fine
                issued_book.return_date = today
                issued_book.save()

        patron.fine += total_fine
        patron.paid = total_fine
        patron.save()

    messages.success(request, f"All books for {patron.name} have been returned.")
    return redirect('search_app:issue_patron', id=patron.id)


# history of mylibrary
def all_history(request):
    history_type = request.GET.get('type', None)
    if history_type == 'all_books':
        t_books = Book_details.objects.all().order_by('-id')
        context = {'t_books': t_books}
        template = 'history.html'
    elif history_type == 'issued_books':
        t_issued_books = IssuedBook.objects.filter(returned=False).order_by('-id')
        context = {'t_issued_books': t_issued_books}
        template = 'history.html'
    elif history_type == 'returned_books':
        t_returned_books = IssuedBook.objects.filter(returned=True).order_by('-id')
        context = {'t_returned_books': t_returned_books}
        template = 'history.html'
    elif history_type == 'patrons':
        t_patrons = Patron.objects.all().order_by('-id')
        context = {'t_patrons': t_patrons}
        template = 'history.html'
    elif history_type == 'categories':
        t_categories = Category.objects.all().order_by('-id')
        context = {'t_categories': t_categories}
        template = 'history.html'
    elif history_type == 'notifications':
        t_notify = Notifications.objects.all().order_by('-id')
        context = {'t_notify': t_notify}
        template = 'history.html'
    elif history_type == 'newspaper':
        t_news = Newspaper.objects.all().order_by('-id')
        context = {'t_news': t_news}
        template = 'history.html'
    elif history_type == 'cart':
        t_cart = CartItem.objects.filter(active=True).order_by('-id')
        context = {'t_cart': t_cart}
        template = 'history.html'
    elif history_type == 'fines':
        patrons = Patron.objects.all()
        t_fines = IssuedBook.objects.filter(patron__in=patrons).order_by('-id')
        context = {'t_fines': t_fines}
        template = 'history.html'
    elif history_type == 'languages':
        t_lang = Language.objects.all().order_by('-id')
        context = {'t_lang': t_lang}
        template = 'history.html'
    elif history_type == 'other':
        # Handle other history types
        template = 'history.html'
        # Set appropriate context if needed
        context = {}
    else:
        # Handle invalid history type or default case
        context = {}
        template = 'all_history.html'
    return render(request, template, context)


def history(request):
    history_type = request.GET.get('type', None)
    category = request.GET.get('category', None)

    if history_type == 'all_books':
        if category:
            t_books = Book_details.objects.filter(category=category).order_by('-id')
        else:
            t_books = Book_details.objects.all().order_by('-id')
        context = {'t_books': t_books}
        template = 'history.html'
    elif history_type == 'issued_books':
        t_issued_books = IssuedBook.objects.filter(returned=False).order_by('-id')
        context = {'t_issued_books': t_issued_books}
        template = 'history.html'
    elif history_type == 'returned_books':
        t_returned_books = IssuedBook.objects.filter(returned=True).order_by('-id')
        context = {'t_returned_books': t_returned_books}
        template = 'history.html'
    elif history_type == 'patrons':
        t_patrons = Patron.objects.all().order_by('-id')
        context = {'t_patrons': t_patrons}
        template = 'history.html'
    elif history_type == 'categories':
        t_categories = Category.objects.all().order_by('-id')
        context = {'t_categories': t_categories}
        template = 'history.html'
    elif history_type == 'notifications':
        t_notify = Notifications.objects.all().order_by('-id')
        context = {'t_notify': t_notify}
        template = 'history.html'
    elif history_type == 'newspaper':
        t_news = Newspaper.objects.all().order_by('-id')
        context = {'t_news': t_news}
        template = 'history.html'
    elif history_type == 'cart':
        t_cart = CartItem.objects.filter(active=True).order_by('-id')
        context = {'t_cart': t_cart}
        template = 'history.html'
    elif history_type == 'fines':
        patrons = Patron.objects.all()
        t_fines = IssuedBook.objects.filter(patron__in=patrons).order_by('-id')
        context = {'t_fines': t_fines}
        template = 'history.html'
    elif history_type == 'languages':
        t_lang = Language.objects.all().order_by('-id')
        context = {'t_lang': t_lang}
        template = 'history.html'
    elif history_type == 'other':
        # Handle other history types
        template = 'history.html'
        # Set appropriate context if needed
        context = {}
    else:
        # Handle invalid history type or default case
        context = {}
        template = 'history.html'

    return render(request, template, context)


def pay_fine(request, id):
    patron = get_object_or_404(Patron, id=id)
    issued_books = IssuedBook.objects.filter(patron=patron)

    if request.method == 'POST':
        amount_paid = request.POST.get('amount_paid')

        if amount_paid is not None and amount_paid != '':
            try:
                amount_paid = Decimal(amount_paid)
                if amount_paid >= 0:
                    total_fine = sum(issued_book.fine for issued_book in issued_books)

                    if amount_paid >= total_fine:
                        patron.paid += total_fine
                        patron.fine = 0

                        for issued_book in issued_books:
                            issued_book.paid += issued_book.fine
                            issued_book.fine = 0
                            issued_book.save()
                    else:
                        patron.paid += amount_paid

                        for issued_book in issued_books:
                            if amount_paid >= issued_book.fine:
                                amount_paid -= issued_book.fine
                                issued_book.paid += issued_book.fine
                                issued_book.fine = 0
                            else:
                                issued_book.paid += amount_paid
                                issued_book.fine -= amount_paid
                                amount_paid = 0

                            issued_book.save()

                        patron.fine = sum(issued_book.fine for issued_book in issued_books)

                    patron.save()

                    messages.success(request, f"All fine has been paid for {patron.name}.")
                else:
                    messages.warning(request, "Please enter a positive amount.")
            except ValueError:
                messages.warning(request, "Invalid amount entered.")
        else:
            messages.warning(request, "Please enter a valid amount.")

    return redirect('search_app:issue_patron', id=patron.id)


def pay_all_fine(request, id):
    patron = get_object_or_404(Patron, id=id)
    issued_books = IssuedBook.objects.filter(patron=patron)

    total_fine = sum(issued_book.fine for issued_book in issued_books)

    for issued_book in issued_books:
        issued_book.paid = issued_book.fine
        issued_book.save()

    if total_fine > 0:
        patron.paid += total_fine
        patron.fine = 0
        patron.save()

        # Update the fine and paid amounts in the issued_books
        for issued_book in issued_books:
            issued_book.patron.paid = issued_book.fine
            issued_book.patron.fine = 0
            issued_book.save()

        messages.success(request, f"All fine has been paid for {patron.name}.")
    else:
        messages.info(request, f"{patron.name} has no fine to pay.")

    return redirect('search_app:issue_patron', id=patron.id)


def calculate_total_fine_for_all_patrons(request):
    id = request.GET.get('id')
    patron = Patron.objects.get(id=id)
    total = IssuedBook.objects.filter(patorn=patron).order_by('-id')
    total_fine = {}
    for result in total:
        patron_fine = result.paid
        total_fine += patron_fine

    context = dict(total_fine=total_fine)
    template = 'home.html'
    return render(request, template, context)
