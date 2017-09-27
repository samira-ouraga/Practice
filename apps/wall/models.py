# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import bcrypt
import re
from django.contrib import messages
from django.db import models

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def val_form(self,request):
        params=request.POST
        if len(params['first_name']) < 3:
            messages.error(request,"First name is too short!")
        if len(params['last_name']) < 2:
            messages.error(request,"Last name is too short!")
        if not EMAIL_REGEX.match(params['email']):
            messages.error(request,"not a valid email")
        if len(User.objects.filter(email=params['email'])) >0:
            messages.error(request, "you already have an account")
        if len(params['password']) < 8:
            messages.error(request,"password has to be at least 8 characters")
        if params['password'] != params['cpassword']:
            messages.error(request,"passwords do not match")
        if len(messages.get_messages(request)) > 0 :
            return False

        hash_password = bcrypt.hashpw(params['password'].encode(),bcrypt.gensalt())
        return self.create(first_name=params['first_name'], last_name=params['last_name'], email=params['email'], password=hash_password)
    
    def val_login(self, request):
        params=request.POST
        if not EMAIL_REGEX.match(params['email']):
            messages.error(request, "not a valid email")
        if len(User.objects.filter(email=params['email'])) <= 0:
            messages.error(request, "you haven't registered yet")
        if len(User.objects.filter(email=params['email'])) > 0:
            password = params['password'].encode()
            hashed = User.objects.get(email=params['email']).password.encode()
            if bcrypt.checkpw(password, hashed)==False:
                messages.error(request, "wrong password")
        if len(messages.get_messages(request)) > 0:
            return False      
        return User.objects.get(email=params['email'])

class User(models.Model):
    first_name = models.CharField( max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField( max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now =True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now =True)

class Author(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now =True)
    books = models.ManyToManyField(Book, related_name="authors")

class Review(models.Model):
    notes = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now =True)
    user = models.ForeignKey(User, related_name="reviews") 
    book = models.ForeignKey(Book, related_name="reviews") 

