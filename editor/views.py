from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login

def login(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to the homepage if already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Redirect after successful login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def home_css_view(request):
    return render(request, 'welcome_page_img.css.html', content_type='text/css')

def custom_404(request, exception):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)

# class HomeView(LoginRequiredMixin, TemplateView):
#     """Authenticated home view."""
#     template_name = "home.html"
#     login_url = "/"  # Redirect to login if not authenticated

def homepage(request):
    return render(request, 'homepage.html')


def custom_logout(request):
    logout(request)
    return redirect('/')  # Redirect to the custom login page

