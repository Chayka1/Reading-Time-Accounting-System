from django.shortcuts import render

from books.models import Book


def main(request):
    return render(request, "main.html")


def reg(request):
    return render(request, "reg.html")


def login(request):
    return render(request, "login.html")


def book_list(request):
    books = Book.objects.all()
    return render(request, "book_list.html", {"books": books})
