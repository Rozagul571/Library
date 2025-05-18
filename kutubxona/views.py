from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import User, Book, Order, Rating
from .serializers import (
    CustomTokenObtainPairSerializer, UserSignupSerializer,
    UserRegisterSerializer, BookSerializer, OrderSerializer, RatingSerializer
)
from .permissions import IsAdmin, IsOperatorOrAdmin, IsUser
from django.utils import timezone
from decimal import Decimal

@extend_schema(tags=['Authentication'])
class TokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK and request.user.is_authenticated:
                response.data['role'] = request.user.role
            return response
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Authentication'])
class TokenRefreshView(TokenRefreshView):
    pass

@extend_schema(tags=['User'])
class UserSignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()

@extend_schema(tags=['User'])
class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        serializer.save()

@extend_schema(tags=['Book'])
class BookListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response({"message": "Book list", "data": serializer.data})

@extend_schema(tags=['Book'])
class BookCreateView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsOperatorOrAdmin]

    def perform_create(self, serializer):
        serializer.save()

@extend_schema(tags=['Book'])
class BookUpdateView(APIView):
    permission_classes = [IsOperatorOrAdmin]

    def put(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Book updated", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Book'])
class BookDeleteView(APIView):
    permission_classes = [IsOperatorOrAdmin]

    def delete(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        book.delete()
        return Response({"message": "Book deleted"}, status=status.HTTP_204_NO_CONTENT)

@extend_schema(tags=['Order'])
class OrderCreateView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            reserve_time=timezone.now(),
            status=Order.Statuses.RESERVED
        )

@extend_schema(tags=['Order'])
class OrderCheckView(APIView):
    permission_classes = [IsAuthenticated]  # Admin va User uchun ochiq

    def get(self, request, *args, **kwargs):
        one_day_ago = timezone.now() - timezone.timedelta(days=1)
        orders_to_cancel = Order.objects.filter(
            user=self.request.user,
            status=Order.Statuses.RESERVED,
            reserve_time__lt=one_day_ago
        )
        for order in orders_to_cancel:
            order.status = Order.Statuses.RETURNED
            order.save()
        active_orders = Order.objects.filter(
            user=self.request.user,
            status__in=[Order.Statuses.RESERVED, Order.Statuses.TAKEN]
        )
        serializer = OrderSerializer(active_orders, many=True)
        return Response({"message": "Active orders checked", "data": serializer.data})

@extend_schema(tags=['Order'])
class OrderListView(APIView):
    permission_classes = [IsOperatorOrAdmin]

    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response({"message": "Order list", "data": serializer.data})

@extend_schema(tags=['Order'])
class OrderTakeView(APIView):
    permission_classes = [IsOperatorOrAdmin]

    def post(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        if order.status != Order.Statuses.RESERVED:
            return Response({"message": "Order cannot be taken"}, status=status.HTTP_400_BAD_REQUEST)
        order.taken_time = timezone.now()
        order.status = Order.Statuses.TAKEN
        order.save()
        serializer = OrderSerializer(order)
        return Response({"message": "Order taken", "data": serializer.data}, status=status.HTTP_200_OK)

@extend_schema(tags=['Order'])
class OrderReturnView(APIView):
    permission_classes = [IsOperatorOrAdmin]

    def post(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        if order.status != Order.Statuses.TAKEN:
            return Response({"message": "Order cannot be returned"}, status=status.HTTP_400_BAD_REQUEST)
        book = order.book
        daily_price = book.daily_price
        return_time = timezone.now()
        delay_days = (return_time - order.taken_time).days
        fine = Decimal('0.00')
        if delay_days > 0:
            fine = Decimal(delay_days) * (daily_price * Decimal('0.01'))
        order.return_time = return_time
        order.fine = fine
        order.status = Order.Statuses.RETURNED
        order.save()
        serializer = OrderSerializer(order)
        return Response({"message": "Order returned", "fine": float(fine), "data": serializer.data}, status=status.HTTP_200_OK)

@extend_schema(tags=['Rating'])
class RatingCreateView(CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)