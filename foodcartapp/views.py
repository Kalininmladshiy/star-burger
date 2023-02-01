import json
from rest_framework import status
from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .models import Product, Order, OrderItem


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    try:
        order = request.data
    except ValueError:
        return Response({
            'error': 'Ошибка в значениях',
        })
    print(order)
    new_order = Order.objects.create(
        customer_name=order['firstname'],
        customer_lastname=order.get('lastname', ''),
        phonenumber=order['phonenumber'],
    )
    if (order.get('products')
        and isinstance(order['products'], list)
            and len(order['products']) != 0):
        for product_in_order in order['products']:
            quantity = product_in_order['quantity']
            product = Product.objects.get(
                id=product_in_order['product'],
            )
            OrderItem.objects.create(
                order=new_order,
                quantity=quantity,
                product=product,
            )
        return Response(request.data)
    else:
        content = {'error': 'products key not presented or not list'}
        return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
