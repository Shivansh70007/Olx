from django.urls import path
from .views import ProductListView , RegisterView , LoginView , ProductCreateView , CartView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('cart/', CartView.as_view(), name='cart'),
    
    # Other API endpoints can be added here
]

