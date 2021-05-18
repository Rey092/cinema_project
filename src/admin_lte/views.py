from django.shortcuts import render


def admin_lte_home(request):
    return render(request, 'admin_lte/pages/home.html')
