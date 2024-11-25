from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path('add-product/', views.add_product, name='add_product'),
    path('products/', views.product_list, name='product_list'),
    path('products/update/<int:pk>/', views.update_product, name='update_product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),

# sales crud
    path('sales/', views.sale_list, name='sale_list'),
    path('sales/add/', views.add_sale, name='add_sale'),
    path('sales/update/<int:pk>/', views.update_sale, name='update_sale'),
    path('sales/delete/<int:pk>/', views.delete_sale, name='delete_sale'),


]
