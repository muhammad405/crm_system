from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Product, Customer, Order, OrderItem
from django.forms import inlineformset_factory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'stock', 'image']
        labels = {
            'name': 'Nomi',
            'category': 'Kategoriya',
            'price': 'Narxi (so\'m)',
            'stock': 'Zaxira (dona)',
            'image': 'Rasm',
        }


    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Narx 0 dan kichik bo'lmasligi kerak!")
        return price

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email']
        labels = {
            'name': 'Ism',
            'phone': 'Telefon',
            'email': 'Email',
        }





class CustomUserCreationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_username(self):
        return self.cleaned_data.get('username')

    def clean_password1(self):
        return self.cleaned_data.get('password1')

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1']
        )
        return user

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'total_amount', 'status']
        labels = {
            'customer': 'Mijoz',
            'total_amount': 'Jami summa (so\'m)',
            'status': 'Status',
        }

OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    fields=('product', 'quantity', 'price'),
    extra=1,
    can_delete=True
)



class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise forms.ValidationError("Miqdor 0 dan kichik bo‘lmasligi kerak!
")
        return quantity

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Narx 0 dan kichik bo‘lmasligi kerak!")
        return price

# Formsetni yangi forma bilan almashtirish
OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, 
extra=1, can_delete=True)
