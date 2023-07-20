from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Newspaper(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True)
    pdf = models.FileField(upload_to='pdfs')

    class Meta:
        ordering = ('name',)
        verbose_name = 'newspaper'
        verbose_name_plural = 'newspapers'

    def __str__(self):
        return '{}'.format(self.name)


class Language(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'language'
        verbose_name_plural = 'languages'

    def __str__(self):
        return '{}'.format(self.name)


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return '{}'.format(self.name)

    def get_url(self):
        if self.slug:
            return reverse('mylibrary:books_by_category', args=[self.slug])
        else:
            return reverse('mylibrary:books_by_category', args=['empty-slug'])

    def update_name(self, new_name):
        # Update the name and slug fields
        self.name = new_name
        self.slug = slugify(new_name)
        self.save()


class Patron(models.Model):
    card_no = models.IntegerField(unique=True)
    name = models.CharField(max_length=250, unique=True)
    phone = models.IntegerField()
    gmail = models.EmailField()
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ('card_no',)
        verbose_name = 'patron'
        verbose_name_plural = 'patrons'

    def total_patron_fine(self):
        return self.paid + self.fine

    def total(self):
        paid = self.paid > 0
        if paid:
            return self.paid + self.fine
        else:
            return 0

    def __str__(self):
        return '{}'.format(self.name)


class Book_details(models.Model):
    primary_number = models.IntegerField(unique=True)
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Book_details, self).save(*args, **kwargs)

    author = models.CharField(max_length=250)
    desc = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    stock = models.IntegerField(default=20)
    pdf = models.FileField(upload_to='pdfs', null=True)
    lang = models.ForeignKey(Language, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_issued = models.BooleanField(default=False)
    issued_to = models.ForeignKey(Patron, on_delete=models.SET_NULL, null=True)
    issue_date = models.DateField(blank=True, null=True)
    download_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('name',)
        verbose_name = 'book_detail'
        verbose_name_plural = 'book_details'

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('mylibrary:book_category_details', args=[self.category.slug, self.slug])

    def increment_download(self):
        self.download_count += 1
        self.save()


class IssuedBook(models.Model):
    book = models.ForeignKey(Book_details, on_delete=models.CASCADE)
    patron = models.ForeignKey(Patron, on_delete=models.CASCADE)
    issue_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    renewal_count = models.IntegerField(default=0)
    returned = models.BooleanField(default=False)
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Issued Book: {self.book.name} - Patron: {self.patron.name}"

    def total(self):
        if self.fine > 0:
            return self.fine - self.paid
        else:
            return 0.0


class Notifications(models.Model):
    name = models.CharField(max_length=250)
    on = models.DateTimeField(verbose_name='Date and Time')
    location = models.CharField(max_length=250)
    inauguration = models.CharField(max_length=250)
    welcome_speech = models.CharField(max_length=250)
    presidential_speech = models.CharField(max_length=250)
    greetings = models.CharField(max_length=250)
    special_speech = models.CharField(max_length=250, null=True)
    speech = models.CharField(max_length=250)
    song = models.CharField(max_length=250)
    vote_of_thanks = models.CharField(max_length=250, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'

    def __str__(self):
        return '{}'.format(self.name)
