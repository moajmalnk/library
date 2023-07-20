from django.contrib import admin
from .models import *

admin.site.register([Language, Category, Book_details, Patron, Newspaper, IssuedBook, Notifications])
