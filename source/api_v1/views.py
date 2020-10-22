from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from api_v1.serializer import ProductSerializer, OrderSerializer, OrderProductSerializer
from webapp.models import Product, Order, OrderProduct, Cart


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class ProductView(APIView):
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return super().get_permissions()

    def get(self, request, pk=None):
        if pk:
            objects = get_object_or_404(Product, pk=pk)
            slr = ProductSerializer(objects, context={'request': request})
        else:
            objects = Product.objects.all()
            slr = ProductSerializer(objects, many=True)
        return Response(slr.data)

    def post(self,request):
        product = request.data
        serializer = ProductSerializer(data=product)
        if serializer.is_valid(raise_exception=True):
            product_saved = serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def put(self, request, pk):
        product = get_object_or_404(Product.objects.all(), pk=pk)
        data = request.data
        serializer = ProductSerializer(instance=product, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            product = serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)


    def delete(self, request, pk):
        product = get_object_or_404(Product.objects.all(), pk=pk)
        product.delete()
        return Response({
            "message": "Продукт с id {} удален".format(pk)
            }, status=204)


class OrderView(APIView):
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            return []
        return super().get_permissions()

    def get(self, request, pk= None):
        if pk:
            objects = get_object_or_404(Order.objects.all(), pk=pk)
            slr = OrderSerializer(objects)
        else:
            objects = Order.objects.all()
            slr = OrderSerializer(objects, many=True)
        return Response(slr.data)

    def post(self, request):
        data = request.data
        order = Order.objects.create(name=data['name'],address=data['address'],phone=data['phone'])
        cart_ids = self.request.session.get('cart_ids', [])
        for i in cart_ids:
            cart = get_object_or_404(Cart, pk=i)
            order_product = OrderProduct.objects.create(product_id=cart.product_id, order_id= order.pk, qty=cart.qty)
        return Response({"message": "Заказ создан"}, status=204)