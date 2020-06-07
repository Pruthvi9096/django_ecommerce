from django.shortcuts import render
from .models import Customer,Order,OrderItem,Product,ShippingAddress

def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
    items_count = 0
    total_price = 0
    if items:
        items_count = sum([item.quantity for item in items])
        total_price = sum([item.product.price*item.quantity for item in items])
    context = {'items':items,'items_count':items_count,'total_price':total_price}
    print(context)
    return render(request, 'store/cart.html', context)

def checkout(request):
      context = {}
      return render(request, 'store/checkout.html', context)
