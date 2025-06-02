from django.shortcuts import render

def home(request):
    return render(request, 'common/home-page.html')

def page_404(request, exception):
    return render(request, '404.html', status=404)