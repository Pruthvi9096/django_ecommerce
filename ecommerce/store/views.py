from django.shortcuts import render
from .models import Customer,Order,OrderItem,Product,ShippingAddress
from django.http import JsonResponse
import datetime
import json

from .utils import cookieCart

def store(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer=customer,complete=False)
    else:
        cart = cookieCart(request)
        order = cart['order']
    context = {'products':products,'order':order}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
    else:
        cart = cookieCart(request)
        order = cart['order']
        items = cart['items']

    context = {'items':items,'order':order}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
    else:
        cart = cookieCart(request)
        order = cart['order']
        items = cart['items']

    context = {'items':items,'order':order}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data.get('productId')
    action = data.get('action')

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, create = Order.objects.get_or_create(customer=customer,complete=False)
    orderitem, itemcreate = OrderItem.objects.get_or_create(product=product,order=order)
    print(customer,order,orderitem)
    if action == 'add':
        orderitem.quantity += 1
    elif action == 'remove':
        orderitem.quantity -= 1

    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()

    return JsonResponse("Item was added",safe=False)

def ProcessOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer=customer,complete=False)

    else:
        print("User is not authenticated!")
        name = data['form']['name']
        email = data['form']['email']
        cart = cookieCart(request)
        items = cart['items']

        customer, created = Customer.objects.get_or_create(email=email)
        customer.name = name
        customer.save()

        order = Order.objects.create(customer=customer,complete=False)

        for item in items:
            product = Product.objects.get(id=item['product']['id'])

            orderItem = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity']
            )
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if order.get_total_price == total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse("Order Is Processed",safe=False)