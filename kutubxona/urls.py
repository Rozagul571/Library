from django.urls import path
from .views import (
    TokenObtainPairView, TokenRefreshView,
    UserSignupView, UserCreateView,
    BookListView, BookCreateView, BookUpdateView, BookDeleteView,
    OrderCreateView, OrderCheckView, OrderListView, OrderTakeView, OrderReturnView,
    RatingCreateView
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/signup/', UserSignupView.as_view(), name='user-signup'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/check/', OrderCheckView.as_view(), name='order-check'),
    path('orders/<int:pk>/take/', OrderTakeView.as_view(), name='order-take'),
    path('orders/<int:pk>/return/', OrderReturnView.as_view(), name='order-return'),
    path('ratings/create/', RatingCreateView.as_view(), name='rating-create'),
]