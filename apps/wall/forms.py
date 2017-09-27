from django import forms 
import datetime
from models import Author


class RegistrationForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=100)
    cpassword = forms.CharField(label='Confirm password', max_length=100)


class LoginForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=100)
    
class AddForm(forms.Form):
    title = forms.CharField(label='Title:', max_length=100)
    author = forms.ModelChoiceField(required=False, queryset=Author.objects.values_list('name', flat=True).order_by('name'))
    newauthor = forms.CharField(required=False, label='New Author:', max_length=100)
    review = forms.CharField(label='Review:', widget=forms.Textarea)

class ReviewForm(forms.Form):
    review = forms.CharField(label='Review:', widget=forms.Textarea)
