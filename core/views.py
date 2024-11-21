from django.shortcuts import render, redirect
from . forms import ProductForm

# Create your views here.

def home(request):
    return render(request, "core/home.html", {})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  
    else:
        form = ProductForm()
    return render(request, 'core/add_product.html', {'form': form})
