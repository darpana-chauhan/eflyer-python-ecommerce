from importlib.metadata import requires

from django.contrib.auth import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
#from myapp.models import AddProduct

class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Sub_Category(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# noinspection PyRedeclaration
class AddProduct(models.Model):

    image = models.ImageField(upload_to='ecommerce/pimg')
    name = models.CharField(max_length=100)
    description=models.CharField(max_length=2000)
    price = models.IntegerField()
    date = models.DateField()
    category = models.ForeignKey(to='Category', default='',on_delete=models.CASCADE)  # ✅ Corrected
    sub_category = models.ForeignKey(to='Sub_Category',default='', on_delete=models.CASCADE)  # ✅ Corrected

    def __str__(self):
        return self.name

class UserCreateForm(UserCreationForm):
    email=forms.EmailField(required=True,label='Email',error_messages={'exists':'This Already Exists'})
    class Meta:
        model=User
        fields=('username','email','password1','password2')
    def __init__(self, *args, **kwargs):
        super(UserCreateForm,self).__init__(*args,**kwargs)

        self.fields['username'].widget.attrs['placeholder']='User Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

    def save(self,commit=True):
        user=super(UserCreateForm,self).save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']

class Cart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cart/images', null=True, blank=True)  # ✅ Corrected
    product = models.ForeignKey(AddProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        """ Automatically set image from product if not provided """
        if not self.image:
            # noinspection PyUnresolvedReferences
            self.image = self.product.image
        super().save(*args, **kwargs)
    def total_price(self):
        # noinspection PyUnresolvedReferences
        return self.product.price * self.quantity

    def __str__(self):
        # noinspection PyUnresolvedReferences
        return f"{self.user.username} - {self.product.name} ({self.quantity})"

class Order(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(AddProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

