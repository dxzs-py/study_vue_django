from rest_framework.permissions import IsAuthenticated

from .models import Order
from rest_framework.generics import CreateAPIView
from .serializers import OrderModelSerializer
# Create your views here.
class OrderAPIView(CreateAPIView):
    """订单视图"""
    queryset = Order.objects.filter(is_deleted=False, is_show=True)
    serializer_class = OrderModelSerializer
    permission_classes = [IsAuthenticated]