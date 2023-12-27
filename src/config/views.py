from django.shortcuts import render


def main(request):
    return render(request, "main.html")


def reg(request):
    return render(request, "reg.html")


def login(request):
    return render(request, "login.html")
