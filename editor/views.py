from django.shortcuts import render


# Create your views here.
def login(request):
    return render(request, 'login.html')


def custom_404(request, exception):
    return render(request, 'template/404.html', status=404)

def custom_500(request):
    return render(request, 'template/500.html', status=500)