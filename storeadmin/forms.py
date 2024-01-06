from django import forms
from bookstore.models import *
from django.contrib.auth.models import User
class BookCreationForm(forms.ModelForm):
    class Meta:
        model=Book
        fields='__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'book_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
class AuthorCreation(forms.ModelForm):
    class Meta:
        model=Author
        fields='__all__'
class GenreCreation(forms.ModelForm):
    class Meta:
        model=Genre
        fields='__all__'
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))