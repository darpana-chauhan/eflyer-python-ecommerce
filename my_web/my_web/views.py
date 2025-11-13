from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.db import transaction
import sqlite3
# noinspection PyUnresolvedReferences
from app.models import Category,AddProduct,Contact

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
# noinspection PyUnresolvedReferences
from app.models import UserCreateForm,Category, AddProduct, Cart,Order,OrderItem
from django.contrib.auth.forms import AuthenticationForm
@login_required(login_url="login")
def logout_view(request):
    logout(request)
    request.session.flush()  # Ensures Session is Fully Cleared
    messages.success(request, "You have been logged out.")

    return redirect("homePage")

def homePage(request):
    category = Category.objects.all()
    categoryID = request.GET.get('category')
    subCategoryID = request.GET.get('sub_category')
    if categoryID and subCategoryID:
        product = AddProduct.objects.filter(category_id=categoryID, sub_category_id=subCategoryID)
    elif categoryID:
        product = AddProduct.objects.filter(category_id=categoryID)
    else:
        product = AddProduct.objects.all()

    context = {
        'category': category,
        'product': product,
    }
    return render(request, "index.html", context)
def jewellery(request):
    return render(request,"jewellery.html")
def electronic(request):
    return render(request,"electronic.html")
def fashion(request):
    return render(request,"fashion.html")
def about(request):
    return render(request,"about.html")
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        #  Data ko database me store karein
        Contact.objects.create(name=name, email=email, subject=subject, message=message)

        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")  #  Form submit hone ke baad wahi page reload hoga

    return render(request, "contact.html")
def product_detail(request, product_id):
    """Display full product details with an option to add to cart."""
    product = get_object_or_404(AddProduct, id=product_id)
    return render(request, "cart/product_detail.html", {"product": product})

def signup(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            login(request, user)  # Log the user in immediately after registration
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect("homePage")  # Redirect to homepage
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreateForm()  # Empty form for GET request

    return render(request, "registration/signup.html", {"form": form})
@login_required(login_url="accounts/login")
def buy_now(request, product_id):
    """Handles adding a product to the cart and redirects to checkout."""
    product = get_object_or_404(AddProduct, id=product_id)

    # Fetch or create cart item for the logged-in user
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    # If item already exists, update quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} has been added to your cart.")

    return redirect("homePage")  # Redirect to cart page instead of homepage
@login_required(login_url="accounts/login")

@login_required(login_url="accounts/login")
def cart_detail(request):
    """Displays the user's cart with items."""
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    cart_count = cart_items.count()  #  Calculate cart count

    return render(request, "cart/cart.html", {
        "cart_items": cart_items,
        "total_price": total_price,
        "cart_count": cart_count,  #  Pass cart count to template
    })

def cart_count(request):
    """Returns the cart count for the logged-in user."""
    if request.user.is_authenticated:
        count = Cart.objects.filter(user=request.user).count()
    else:
        count = 0
    return {"cart_count": count}


@login_required(login_url="accounts/login")
def update_cart(request, cart_id):
    """Updates the quantity of a product in the cart."""
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)

    if request.method == "POST":
        new_quantity = int(request.POST.get("quantity", 1))

        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, "Cart updated successfully!")
        else:
            cart_item.delete()
            messages.success(request, "Item removed from cart.")

    return redirect("cart_detail")

@login_required(login_url="accounts/login")
def remove_cart_item(request, item_id):
    """Removes an item from the cart."""
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    return redirect("cart_detail")  # Redirect back to the cart page


@login_required(login_url="accounts/login")
def checkout(request, product_id=None):
    """Handles checkout for a single product from the cart."""
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("cart_detail")

    total_price = sum(item.total_price() for item in cart_items)

    if request.method == "POST":
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                total_price=total_price,
                address=address,
                phone=phone
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )

            cart_items.delete()  # sabhi items remove kar do cart se

        messages.success(request, "Your order has been placed successfully!")
        return redirect("order_summary")

    return render(request, "cart/chackout.html", {
        "cart_items": cart_items,
        "total_price": total_price,
    })

@login_required(login_url="accounts/login")
def order_summary(request):
    """Show all orders for the logged-in user with details."""
    user_orders = Order.objects.filter(user=request.user).prefetch_related("items")

    orders_data = []
    for order in user_orders:
        for order_item in order.items.all():  # ✅ Fetch OrderItem instead of Cart
            orders_data.append({
                "order_id": order.id,
                "product_name": order_item.product.name,
                "quantity": order_item.quantity,
                "price": order_item.total_price(),
                "status": order.status,
                "created_at": order.created_at,
            })

    return render(request, "cart/order.html", {
        "orders": orders_data,
        "user_name": request.user.username,
    })

@login_required(login_url="accounts/login")
def add_to_cart(request, product_id):
    """Handles adding a product with selected quantity to the cart."""
    product = get_object_or_404(AddProduct, id=product_id)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))

        # Fetch or create the cart item for the user
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

        # Update quantity if already in cart
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.total_price=cart_item.quantity*product.price
        cart_item.save()

        messages.success(request, f"{product.name} ({quantity}) added to your cart!")
        return redirect("homePage")  # ✅ Stay on the homepage after adding to cart

    return redirect("product_detail", product_id=product.id)
