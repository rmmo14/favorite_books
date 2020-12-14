from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('books', views.books),
    path('logout', views.logout),
    path('add_book', views.add_book),
    path('books/<int:book_id>', views.bookinfo),
    path('books/<int:book_id>/update', views.update),
    path("books/<int:book_id>/delete", views.delete),
    path("favorite/<int:book_id>", views.favorite),
    path("unfavorite/<int:book_id>", views.unfavorite),
]