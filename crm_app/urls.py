from django.urls import path
from . import views
from django.shortcuts import render, get_object_or_404
from .models import Product

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('customers/', views.customer_list, name='customer_list'),
    path('orders/', views.order_list, name='order_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('register/', views.register, name='register'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('customers/add/', views.add_customer, name='add_customer'),
    path('customers/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('orders/add/', views.add_order, name='add_order'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),  # Yangi
    path('customers/<int:pk>/delete/', views.delete_customer, name='delete_customer'),  # Yangi
    path('orders/<int:pk>/delete/', views.delete_order, name='delete_order'),
    path('logout/', views.logout_view, name='logout'),
    path('orders/delete/<int:pk>/', views.delete_order, name='delete_order'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),

]

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'crm/product_detail.html', {'product': product})