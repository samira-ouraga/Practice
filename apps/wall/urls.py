from django.conf.urls import url
from . import views

urlpatterns= [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^books$', views.books, name='books'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^add$', views.add, name='add'),
    url(r'^create$', views.create, name='create'),
    url(r'^review/(?P<book_number>\d+)$', views.review, name='review'),
    url(r'^delete_review/(?P<review_id>\d+)$', views.delete_review, name='delete_review'),
    url(r'^user/(?P<user_number>\d+)$', views.user, name='user'),
    url(r'^book/(?P<book_number>\d+)$', views.book, name='book'),

    
]