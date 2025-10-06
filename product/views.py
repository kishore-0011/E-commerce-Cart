from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product
from .cart import Cart
from .froms import CartAddProductForm

def product_list(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Price filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Sort
    sort = request.GET.get('sort')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    
    context = {
        'products': products,
        'categories': categories,
        'query': query or '',
        'selected_category': category_slug or '',
        'min_price': min_price or '',
        'max_price': max_price or '',
        'sort': sort or '',
    }
    return render(request, 'product/product_list.html', context)

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        quantity = cd['quantity']
        
        # Check stock availability
        if product.stock < quantity:
            messages.error(request, f'Only {product.stock} units available in stock.')
            return redirect('shop:product_list')
        
        cart.add(product=product, quantity=quantity, override_quantity=cd['override'])
        messages.success(request, f'{product.name} added to cart!')
    
    # Return JSON response for AJAX or redirect for regular form
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        from django.http import JsonResponse
        return JsonResponse({'cart_count': len(cart)})
    
    return redirect('shop:product_list')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'{product.name} removed from cart!')
    
    # Return JSON response for AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        from django.http import JsonResponse
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'cart_total': str(cart.get_total_price())
        })
    
    return redirect('shop:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'product/cart.html', {'cart': cart})

@require_POST
def cart_update_quantity(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    action = request.POST.get('action')
    
    current_quantity = cart.cart.get(str(product_id), {}).get('quantity', 0)
    
    if action == 'increase':
        new_quantity = current_quantity + 1
        if new_quantity > 10:
            messages.error(request, 'Maximum quantity limit is 10!')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                from django.http import JsonResponse
                return JsonResponse({'success': False, 'error': 'Maximum quantity limit is 10!'})
            return redirect('shop:cart_detail')
        if new_quantity > product.stock:
            messages.error(request, f'Only {product.stock} units available in stock!')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                from django.http import JsonResponse
                return JsonResponse({'success': False, 'error': f'Only {product.stock} units available in stock!'})
            return redirect('shop:cart_detail')
        cart.add(product=product, quantity=new_quantity, override_quantity=True)
    
    elif action == 'decrease':
        new_quantity = current_quantity - 1
        if new_quantity < 1:
            messages.error(request, 'Minimum quantity is 1!')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                from django.http import JsonResponse
                return JsonResponse({'success': False, 'error': 'Minimum quantity is 1!'})
            return redirect('shop:cart_detail')
        cart.add(product=product, quantity=new_quantity, override_quantity=True)
    
    # Return JSON response for AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        from django.http import JsonResponse
        from decimal import Decimal
        
        # Get updated item details
        item_total = Decimal(cart.cart[str(product_id)]['price']) * cart.cart[str(product_id)]['quantity']
        
        return JsonResponse({
            'success': True,
            'quantity': cart.cart[str(product_id)]['quantity'],
            'item_total': str(item_total),
            'cart_total': str(cart.get_total_price()),
            'cart_count': len(cart)
        })
    
    return redirect('shop:cart_detail')