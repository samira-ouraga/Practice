# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime
from django import forms
from .forms import RegistrationForm, LoginForm, AddForm, ReviewForm
from .models import User, UserManager, Book, Author, Review

# Create your views here.
def index(request):
    form1 = RegistrationForm()
    form2 = LoginForm()
    return render(request, 'wall/index.html', {'form1': form1, 'form2':form2})

def register(request):
    if request.method == 'POST':
        current_user = User.objects.val_form(request)
        if current_user:
            request.session['current_user_id']= current_user.id
            return redirect('/books')
    return redirect("/")

def login(request):
    if request.method == 'POST':
        current_user = User.objects.val_login(request)
        if current_user:
            request.session['current_user_id']= current_user.id
            return redirect('/books')
    return redirect("/")

def books(request):
    current_user = get_current_user(request)
    context={
        'users' : User.objects.order_by('first_name'),
        'current_user': current_user,
        'books' : Book.objects.order_by('title'),
        'reviews' : Review.objects.all().order_by('-created_at')[:3],
    }
    return render(request, 'wall/books.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def add(request):
    current_user = get_current_user(request)
    context={
        'current_user': current_user.first_name,
        'form3': AddForm(),
    }
    return render(request, 'wall/add.html', context)

def create(request):
    current_user = get_current_user(request)
    if request.method =='POST':
        author_name = request.POST['author']
        author = Author.objects.filter(name=author_name)
        if len(author) > 0:
            author = author[0]
        else:
            author_name = request.POST['newauthor']
            author = Author.objects.filter(name=author_name)
            if len(author) > 0:
                author = author[0]
            else:
                author = Author.objects.create(name = author_name)
        book_title = request.POST['title']
        book = Book.objects.filter(title = book_title)
        print book
        if len(book) > 0 and len(book[0].authors.filter(id=author.id)):
            book = book[0]
            print book
        else:
            book = Book.objects.create(
                title = request.POST['title']
            )
            book.authors.add(author)
            book.save()
            print book
        Review.objects.create(
            user = current_user,
            notes = request.POST['review'],
            book = Book.objects.filter(title = book_title)

        )
        return redirect("/book/{}".format(book.id))
    errors = form3.errors or None # form not submitted or it has errors
    return render(request, 'wall/add.html',{
        'form3': form3,
        'errors': errors,
    })

def review(request, book_number):
    current_user = get_current_user(request)
    current_book = Book.objects.get(id = book_number)
    if request.method =='POST':
        Review.objects.create(
            user = current_user,
            notes = request.POST['review'],
            book = current_book
        )
    return redirect("/book/{}".format(book_number))


def book(request, book_number):
    current_user = get_current_user(request)
    book = Book.objects.get(id = book_number)
    authors = Author.objects.filter(books__id = book_number)
    context={
        'current_user': current_user.first_name,
        'form4': ReviewForm(),
        'users' : User.objects.all(),
        'authors' : authors,
        'current_user': current_user,
        'book' : book,
        'reviews' : Review.objects.filter(book_id = book_number),
        'book_number' : book_number,
    }

    return render(request, 'wall/book.html', context)

def user(request, user_number):
    current_user = get_current_user(request)
    user = User.objects.get(id = user_number)
    review = Review.objects.filter(user_id = user_number)
    context={
        'user' : user,
        'author' : Author.objects.all(),
        'current_user': current_user,
        'books' : Book.objects.all(),
        'reviews' : review,
        'user_number' : user_number,
        'count' : review.count()
    }
    return render(request, 'wall/user.html', context)

def delete_review(request, review_id):
    current_user = get_current_user(request)
    review_id = review_id
    book = Review.objects.get(id=review_id) #has to get the book from the Review model because we have the review id
    instance = Review.objects.filter(id = review_id)
    instance.delete()
    return redirect("/book/{}".format(book.book_id)) #must use book_id because book is a foreign key on the Review model

def get_current_user(request):
    current_user = User.objects.get(id = request.session['current_user_id'])
    return current_user
    