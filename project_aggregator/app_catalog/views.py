from django.http import HttpRequest
from django.shortcuts import render


def index(request: HttpRequest):
    if request.user.is_authenticated:
        name = ' '.join(request.user.full_name.split()[1:])
        print(f'{name} {type(name)}')
    else:
        name = ''
    return render(request, 'index.html', {'name': name})
