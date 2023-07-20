from django import forms

from .models import *


class BookForm(forms.ModelForm):
    class Meta:
        model = Book_details
        fields = ['name', 'author', 'desc', 'category', 'price', 'stock', 'lang']

    def clean_name(self):
        name = self.cleaned_data['name']
        slug = slugify(name)
        # Check if the slug already exists in the database
        if Book_details.objects.filter(slug=slug).exists():
            raise forms.ValidationError('A book with this name already exists.')
        return name

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = slugify(instance.name)
        if commit:
            instance.save()
        return instance


class NewsForm(forms.ModelForm):
    class Meta:
        model = Newspaper
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data['name']
        slug = slugify(name)
        # Check if the slug already exists in the database
        if Newspaper.objects.filter(slug=slug).exists():
            raise forms.ValidationError('A news  with this name already exists.')
        return name

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = slugify(instance.name)
        if commit:
            instance.save()
        return instance


class PatronForm(forms.ModelForm):
    class Meta:
        model = Patron
        fields = ['name', 'phone', 'gmail']


class NotificationsForm(forms.ModelForm):
    class Meta:
        model = Notifications
        fields = [
            'name', 'location', 'inauguration',
            'welcome_speech', 'presidential_speech',
            'greetings', 'special_speech', 'speech',
            'song', 'vote_of_thanks']

    def clean_name(self):
        name = self.cleaned_data['name']
        # Add any additional validation for the name field if needed
        return name
