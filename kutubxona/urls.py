from django.urls import path
from .views import (
    TokenObtainPairView, TokenRefreshView,
    UserSignupViewSet, UserCreateViewSet,
    BookListViewSet, OrderViewSet, RatingViewSet
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('users/signup/', UserSignupViewSet.as_view({'post': 'create'}), name='user-signup'),
    path('users/create/', UserCreateViewSet.as_view({'post': 'create'}), name='user-create'),
    path('users/<int:pk>/', UserCreateViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-detail'),

    path('books/', BookListViewSet.as_view({'get': 'list', 'post': 'create'}), name='book-list'),
    path('books/<int:pk>/', BookListViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='book-detail'),

    path('orders/create/', OrderViewSet.as_view({'post': 'create'}), name='order-create'),
    path('orders/check/', OrderViewSet.as_view({'get': 'check'}), name='order-check'),
    path('orders/<int:pk>/', OrderViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='order-detail'),
    path('orders/<int:pk>/take/', OrderViewSet.as_view({'post': 'take'}), name='order-take'),
    path('orders/<int:pk>/return/', OrderViewSet.as_view({'post': 'return_order'}), name='order-return'),

    path('ratings/create/', RatingViewSet.as_view({'post': 'create'}), name='rating-create'),
    path('ratings/<int:pk>/', RatingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='rating-detail'),
]