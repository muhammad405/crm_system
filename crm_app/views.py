from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, authenticate
from .models import Product, Customer, Order
from .forms import ProductForm, CustomUserCreationForm
from .forms import CustomerForm
from django.contrib.auth import logout
from .forms import OrderForm, OrderItemFormSet
from django.db import models
import json


@login_required(login_url='/register/')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'crm/product_list.html', {'products': products})

@login_required(login_url='/register/')
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'crm/customer_list.html', {'customers': customers})

@login_required(login_url='/register/')
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'crm/order_list.html', {'orders': orders})

@login_required(login_url='/register/')
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'crm/product_detail.html', {'product': product})

@login_required(login_url='/register/')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'crm/add_product.html', {'form': form})

@login_required(login_url='/register/')
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'crm/edit_product.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                if username == 'admin' and password == '1':
                    user = form.save()
                    login(request, user)
                    return redirect('home')
                else:
                    form.add_error(None, "Login yoki parol xato.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



@login_required(login_url='/register/')
def home(request):
    product_count = Product.objects.count()
    total_price = Product.objects.aggregate(total=models.Sum('price'))['total'] or 0
    latest_products = Product.objects.order_by('-id')[:5]
    customer_count = Customer.objects.count()
    order_count = Order.objects.count()
    total_order_amount = Order.objects.aggregate(total=models.Sum('total_amount'))['total'] or 0
    exchange_rate = 12650
    total_order_amount_usd = round(total_order_amount / exchange_rate, 2) if total_order_amount else 0

    categories = Product.objects.values('category').distinct()
    category_prices = {}
    for cat in categories:
        category_total = Product.objects.filter(category=cat['category']).aggregate(total=models.Sum('price'))['total'] or 0
        category_prices[cat['category']] = float(category_total)

    products = Product.objects.order_by('id')
    product_ids = [p.id for p in products]
    product_prices = [float(p.price) for p in products]

    chart_data = {
        'category_prices': category_prices,
        'product_ids': product_ids,
        'product_prices': product_prices
    }

    print("Chart Data:", chart_data)

    return render(request, 'crm/home.html', {
        'product_count': product_count,
        'total_price': total_price,
        'latest_products': latest_products,
        'customer_count': customer_count,
        'order_count': order_count,
        'total_order_amount': total_order_amount,
        'total_order_amount_usd': total_order_amount_usd,
        'chart_data': json.dumps(chart_data)
    })

@login_required(login_url='/register/')
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'crm/add_customer.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/register/')
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'crm/customer_detail.html', {'customer': customer})

@login_required(login_url='/register/')
def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'crm/add_order.html', {'form': form})

@login_required(login_url='/register/')
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'crm/order_detail.html', {'order': order})

@login_required(login_url='/register/')
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'crm/delete_confirm.html', {'object': product, 'type': 'mahsulot'})




@login_required(login_url='/register/')
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'crm/delete_confirm.html', {'object': customer, 'type': 'mijoz'})

@login_required(login_url='/register/')
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'crm/delete_confirm.html', {'object': order, 'type': 'buyurtma'})