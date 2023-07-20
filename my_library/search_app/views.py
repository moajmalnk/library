from django.db.models import Q
from django.shortcuts import render

from mylibrary.models import *


def search_result(request):
    books = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        books = Book_details.objects.filter(
            Q(primary_number__contains=query) |
            Q(name__contains=query) |
            Q(category__name__contains=query) |  # Assuming the related field in the Category model is named 'name'
            Q(lang__name__contains=query) |  # Assuming the related field in the Language model is named 'name'
            Q(slug__contains=query) |
            Q(desc__contains=query) |
            Q(author__contains=query) |
            Q(price__contains=query)
        )
    context = {
        'query': query,
        'book_s': books
    }
    return render(request, 'search.html', context)


def patrons(request):
    patron = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        patron = Patron.objects.all().filter(
            Q(name__contains=query) |
            Q(gmail__contains=query) |
            Q(card_no__contains=query) |
            Q(phone__contains=query)
        )
    context = {
        'query': query,
        's_patron': patron
    }
    return render(request, 'search.html', context)
