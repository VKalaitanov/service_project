from django.shortcuts import render


def home(request):
    return render(request, 'service/index.html')


def about(request):
    return render(
        request,
        'service/about.html',
    )