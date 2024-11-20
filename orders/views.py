from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from notifications.emails import send_order_confirmation, send_shipping_update, send_payment_receipt
class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderUpdateStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        # Check if the user is a seller or admin
        if request.user.role not in ['seller', 'admin']:
            return Response(
                {"error": "You do not have permission to update order status."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Fetch the order
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        # Validate the status value
        status_value = request.data.get('status')
        valid_statuses = [status[0] for status in Order.ORDER_STATUS_CHOICES]

        if status_value not in valid_statuses:
            return Response({"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the order status
        order.status = status_value
        order.save()

        return Response({"status": "Order status updated successfully."}, status=status.HTTP_200_OK)
    '''def confirm_order(request, order_id):
        order = Order.objects.get(id=order_id)
        user = request.user
        send_order_confirmation(user, order)
    # Additional logic for order confirmation
        return Response({"message": "Order confirmed and notification sent."})

    def update_shipping_status(request, order_id):
        order = Order.objects.get(id=order_id)
        user = request.user
        send_shipping_update(user, order)
    # Additional logic for shipping update
        return Response({"message": "Shipping status updated and notification sent."})'''
