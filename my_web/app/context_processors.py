from app.models import Cart

def cart_count(request):
    """Returns the cart count for the logged-in user."""
    if request.user.is_authenticated:
        count = Cart.objects.filter(user=request.user).count()
    else:
        count = 0
    return {"cart_count": count}
