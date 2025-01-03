from django.shortcuts import render

# # Create your views here.
# from rest_framework import generics
# from .models import Product
# from .serializers import ProductSerializer
# from django.db.models import Q
# from rest_framework.filters import BaseFilterBackend

# # Custom filter backend to handle the filtering logic
# class ProductFilterBackend(BaseFilterBackend):
#     def filter_queryset(self, request, queryset, view):
#         price_min = request.GET.get('price_min')
#         price_max = request.GET.get('price_max')
#         category = request.GET.get('category')
#         year = request.GET.get('year')
#         brand = request.GET.get('brand')
#         area = request.GET.get('area')

#         filters = Q()

#         if price_min and price_max:
#             filters &= Q(price__gte=price_min, price__lte=price_max)
#         if category:
#             filters &= Q(category__icontains=category)
#         if year:
#             filters &= Q(year=year)
#         if brand:
#             filters &= Q(brand__icontains=brand)
#         if area:
#             filters &= Q(area__icontains=area)

#         return queryset.filter(filters)


# # Create a ListAPIView to handle product listing and filtering
# class ProductListView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [ProductFilterBackend]



from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Product , CartItem
from .serializers import ProductSerializer , LoginSerializer , CartItemSerializer
from rest_framework.permissions import IsAuthenticated , AllowAny , IsAdminUser
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework import status
# from rest_framework_simplejwt.tokens import Untoken

class ProductListView(APIView):
    # permission_classes=[IsAuthenticated]    # ----> this should be at this level for authentication application
    
    # i've commented out above line since evryone can see the products but only logged in can post and add a 
    # product to the cart
    def get(self, request):
        products = Product.objects.all()
        
        # Get filter parameters from the request
        category = request.GET.get('category')
        price_min = request.GET.get('priceMin')
        price_max = request.GET.get('priceMax')
        year = request.GET.get('year')
        brand = request.GET.get('brand')
        area = request.GET.get('area')
         # Debugging: Print filter parameters
        print(f"Filtering with price_min: {price_min}, price_max: {price_max}")
        print(f"Other filters - Category: {category}, Brand: {brand}, Year: {year}, Area: {area}")

        # Apply filters based on provided parameters
        if price_min:
            try:
                price_min = float(price_min)
                products = products.filter(price__gte=price_min)
            except ValueError:
                pass

        if price_max:
            try:
                price_max = float(price_max)
                products = products.filter(price__lte=price_max)
            except ValueError:
                pass

        if year:
            try:
                year = int(year)
                products = products.filter(year=year)
            except ValueError:
                pass
        if category:
            products = products.filter(category__icontains=category)
        # if price_min:
        #     products = products.filter(price__gte=price_min)
        # if price_max:
        #     products = products.filter(price__lte=price_max)
        # if year:
        #     products = products.filter(year=year)
        if brand:
            products = products.filter(brand__icontains=brand)
        if area:
            products = products.filter(area__icontains=area)
         # Debugging: Print the number of products after applying filters
        print(f"Number of products after filtering: {len(products)}")

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

# User registration view
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({"message": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Create user logic here
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# User login view
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Login successful!',
                'token': token.key
            }, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)




class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        # Get product data from the request
        data = request.data
        data['created_by'] = request.user.id  # Associate the product with the logged-in user
        
        # Serialize the product data
        serializer = ProductSerializer(data=data)
        token = request.headers.get('Authorization', None)
        print("Received Token:", token)

        # Check if data is valid and create product
        if serializer.is_valid():
            serializer.save()  # Save the product instance
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get cart items for the logged-in user
        cart_items = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
    # Add a product to the user's cart
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the product is already in the cart
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += quantity  # Increase quantity if already in the cart
            cart_item.save()

        # Fetch updated cart items and return them
        cart_items = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def delete(self, request):
        # Remove a product from the user's cart
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            cart_item = CartItem.objects.get(user=request.user, product=product)
            cart_item.delete()
            return Response({"message": "Product removed from cart"}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"error": "Product not in cart"}, status=status.HTTP_404_NOT_FOUND)

