from django.shortcuts import render, redirect, get_object_or_404
from . forms import ProductForm, SaleForm
from . models import Product,Sale
from django.db.models import Sum

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


# add sale
def add_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('sale_list')
            except ValueError as e:
                form.add_error('quantity', str(e))
    else:
        form = SaleForm()
    return render(request, 'core/add_sale.html', {'form': form})

# view sales
def sale_list(request):
    sales = Sale.objects.select_related('product').all()
    return render(request, 'core/sale_list.html', {'sales': sales})


# update sale
def update_sale(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    old_quantity = sale.quantity
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            try:
                # Reverse previous stock adjustment
                sale.product.stock += old_quantity
                sale.product.save()
                
                # Save the updated sale
                form.save()
                return redirect('sale_list')
            except ValueError as e:
                form.add_error('quantity', str(e))
    else:
        form = SaleForm(instance=sale)
    return render(request, 'core/add_sale.html', {'form': form})


# delete sale
def delete_sale(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        # Restore stock
        sale.product.stock += sale.quantity
        sale.product.save()
        sale.delete()
        return redirect('sale_list')
    return render(request, 'core/confirm_delete.html', {'sale': sale})


# report
from .models import Product

def sales_report(request):
    # Fetch filters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    product_id = request.GET.get('product_id')

    # Base query
    sales = Sale.objects.all()

    # Apply filters
    if start_date:
        sales = sales.filter(created_at__gte=start_date)
    if end_date:
        sales = sales.filter(created_at__lte=end_date)
    if product_id:
        sales = sales.filter(product__id=product_id)

    # Aggregate data
    total_sales = sales.aggregate(total=Sum('total_price'))['total'] or 0
    total_quantity = sales.aggregate(total=Sum('quantity'))['total'] or 0

    # Get all products for the dropdown
    products = Product.objects.all()

    # Render template
    return render(request, 'core/report.html', {
        'sales': sales,
        'total_sales': total_sales,
        'total_quantity': total_quantity,
        'start_date': start_date,
        'end_date': end_date,
        'product_id': product_id,
        'products': products,
    })
