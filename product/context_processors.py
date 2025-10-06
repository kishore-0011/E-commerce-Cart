from .models import CartItem

def cart_context(request):
    cart_unique_count = 0
    if request.user.is_authenticated:
        # Count unique products, not total quantity
        cart_unique_count = CartItem.objects.filter(user=request.user).count()
    return {'cart_unique_count': cart_unique_count}
