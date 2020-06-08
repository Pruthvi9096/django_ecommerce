import json
from .models import *

def cookieCart(request):
    cart = json.loads(request.COOKIES.get('cart')or '{}')
    items = []
    order = {'get_items_count':0, 'get_total_price':0,'shipping':False}

    for i in cart:
        try:
            order['get_items_count'] += cart[i]['quantity']
            product = Product.objects.get(id=int(i))
            order['get_total_price'] += product.price * cart[i]['quantity']
        
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'digital':product.digital,
                    'imageUrl':product.imageUrl,
                },
                'quantity':cart[i]['quantity'],
                'totalPrice':product.price * cart[i]['quantity']
            }
            items.append(item)
            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    return {'items':items,'order':order}
