from django.shortcuts import render

def sayHello(request) :
    return render(request, "hello.html")
