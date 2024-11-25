from django.shortcuts import render, redirect, get_object_or_404
from . forms import ProductForm
from . models import Product

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

# listing products
def product_list(request):
    products = Product.objects.all()
    return render(request, 'core/product_list.html', {'products': products})

# update functinality
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'core/add_product.html', {'form': form})


# delete functionality
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'core/confirm_delete.html', {'product': product})