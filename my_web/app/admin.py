from django.contrib import admin
from .models import Category, Sub_Category, AddProduct, Cart, Order, OrderItem, Contact

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # ID added

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')  # ID added

class AddProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'sub_category', 'price', 'date')

class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)
        return qs

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'display_order_items', 'created_at')

    def display_order_items(self, obj):
        return ", ".join([f"{item.product.name} (Qty: {item.quantity})" for item in obj.items.all()])

    display_order_items.short_description = "Ordered Items"

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')  # ID added


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'subject', 'created_at')  #ID added


# Proper Sequence Registration
admin.site.register(Category, CategoryAdmin)
admin.site.register(Sub_Category, SubCategoryAdmin)
admin.site.register(AddProduct, AddProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Contact, ContactAdmin)
