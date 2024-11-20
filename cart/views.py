from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from orders.models import Order, OrderItem
from .permissions import IsBuyerOrAdmin

class AddToCartView(APIView):
    #permission_classes = [IsAuthenticated]
    permission_classes = [IsBuyerOrAdmin]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


class RemoveFromCartView(APIView):
    #permission_classes = [IsAuthenticated]
    permission_classes = [IsBuyerOrAdmin]
    def delete(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            cart_item.delete()
            return Response({"message": "Item removed from cart."}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

class CheckoutView(APIView):
    #permission_classes = [IsAuthenticated]
    permission_classes = [IsBuyerOrAdmin]
    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

        items = cart.items_cart.all()
        total_amount = sum(item.product.price * item.quantity for item in items)
        serialized_cart = CartSerializer(cart).data
        cart_data = {
            **serialized_cart,
            "total_amount": total_amount,
        }
        return Response(cart_data, status=status.HTTP_200_OK)

    def post(self, request):
        address = request.data.get('address')
        payment_method = request.data.get('payment_method')

        if not address or not payment_method:
            return Response({"error": "Address and payment method are required."}, status=status.HTTP_400_BAD_REQUEST)

        cart, created = Cart.objects.get_or_create(user=request.user)

        existing_order = cart.get_order()
        if existing_order:
            return Response({"error": f"This cart already has an order with ID {existing_order.id}."}, status=status.HTTP_400_BAD_REQUEST)

        items = cart.items_cart.all()
        if not items.exists():
            return Response({"error": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        total_amount = sum(item.product.price * item.quantity for item in items)

        order = Order.objects.create(
            user=request.user,
            address=address,
            payment_method=payment_method,
            total_amount=total_amount,
            cart=cart
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        cart.items_cart.all().delete()
        cart.save()

        return Response({"order_id": order.id, "status": "Order created"}, status=status.HTTP_201_CREATED)
