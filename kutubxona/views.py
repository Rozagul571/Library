from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import User, Book, Order, Rating
from .serializers import (
    CustomTokenObtainPairSerializer, UserSignupSerializer,
    UserRegisterSerializer, BookSerializer, OrderSerializer, RatingSerializer
)
from .permissions import IsAdmin, IsOperatorOrAdmin, IsUser
from django.utils import timezone

@extend_schema(tags=['Authentication'])
class TokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@extend_schema(tags=['Authentication'])
class TokenRefreshView(TokenRefreshView):
    pass

@extend_schema(tags=['User'])
class UserSignupViewSet(GenericViewSet, CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User created", "data": serializer.data}, status=status.HTTP_201_CREATED)

@extend_schema(tags=['User'])
class UserCreateViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [IsAdmin]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User created by admin", "data": serializer.data}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

@extend_schema(tags=['Book'])
class BookListViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOperatorOrAdmin()]
        return [AllowAny()]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Book created", "data": serializer.data}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

@extend_schema(tags=['Order'])
class OrderViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsUser]

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy', 'take', 'return_order']:
            return [IsOperatorOrAdmin()]
        if self.action in ['create', 'check']:
            return [IsUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=self.request.user,
            reserve_time=timezone.now(),
            status=Order.Statuses.RESERVED
        )
        return Response({"message": "Order created", "data": serializer.data}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'], permission_classes=[IsUser])
    def check(self, request, *args, **kwargs):
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
        serializer = self.get_serializer(active_orders, many=True)
        return Response({"message": "Active orders", "data": serializer.data})

    @action(detail=True, methods=['post'], permission_classes=[IsOperatorOrAdmin])
    def take(self, request, pk=None):
        order = self.get_object()
        if order.status != Order.Statuses.RESERVED:
            return Response({"message": "Order cannot be taken"}, status=status.HTTP_400_BAD_REQUEST)
        order.taken_time = timezone.now()
        order.status = Order.Statuses.TAKEN
        order.save()
        serializer = self.get_serializer(order)
        return Response({"message": "Order taken", "data": serializer.data}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsOperatorOrAdmin])
    def return_order(self, request, pk=None):
        order = self.get_object()
        if order.status != Order.Statuses.TAKEN:
            return Response({"message": "Order cannot be returned"}, status=status.HTTP_400_BAD_REQUEST)
        book = order.book
        daily_price = book.daily_price
        return_time = timezone.now()
        delay_days = (return_time - order.taken_time).days
        fine = 0
        if delay_days > 0:
            fine = delay_days * (daily_price * 0.01)
        order.return_time = return_time
        order.fine = fine
        order.status = Order.Statuses.RETURNED
        order.save()
        serializer = self.get_serializer(order)
        return Response({"message": "Order returned", "fine": fine, "data": serializer.data}, status=status.HTTP_200_OK)

@extend_schema(tags=['Rating'])
class RatingViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsUser]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsUser()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response({"message": "Rating created", "data": serializer.data}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)