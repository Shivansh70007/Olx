#models.py
from django.db import models
from django.contrib.auth.models import User  # Import the User model
# Create your models here.
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    year = models.IntegerField()
    area = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Add the created_by field

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product in the cart
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} in {self.user.username}'s cart"

# # serilizers.py 

# from rest_framework import serializers
# from .models import Product


# # product serializer
# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'description', 'price', 'brand', 'category', 'year', 'area', 'created_at','created_by']


# # Login serializer
# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()

#     def validate(self, data):
#         user = User.objects.filter(username=data['username']).first()
#         if user and user.check_password(data['password']):
#             return user
#         raise serializers.ValidationError('Invalid credentials')
        

# #-------------Products one urls.py
# from django.urls import path
# from .views import ProductListView , RegisterView , LoginView , ProductCreateView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# urlpatterns = [
#     path('products/', ProductListView.as_view(), name='product-list'),
#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/', LoginView.as_view(), name='login'),
#     path('products/create/', ProductCreateView.as_view(), name='product-create'),
#     # Other API endpoints can be added here
# ]

# # views.py

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.db.models import Q
# from .models import Product
# from .serializers import ProductSerializer , LoginSerializer
# from rest_framework.permissions import IsAuthenticated , AllowAny , IsAdminUser
# from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User
# from rest_framework.permissions import AllowAny
# from rest_framework import status

# class ProductListView(APIView):
#     # permission_classes=[IsAuthenticated]    # ----> this should be at this level for authentication application
    
#     # i've commented out above line since evryone can see the products but only logged in can post and add a 
#     # product to the cart
#     def get(self, request):
#         products = Product.objects.all()
        
#         # Get filter parameters from the request
#         category = request.GET.get('category')
#         price_min = request.GET.get('priceMin')
#         price_max = request.GET.get('priceMax')
#         year = request.GET.get('year')
#         brand = request.GET.get('brand')
#         area = request.GET.get('area')
#          # Debugging: Print filter parameters
#         print(f"Filtering with price_min: {price_min}, price_max: {price_max}")
#         print(f"Other filters - Category: {category}, Brand: {brand}, Year: {year}, Area: {area}")

#         # Apply filters based on provided parameters
#         if price_min:
#             try:
#                 price_min = float(price_min)
#                 products = products.filter(price__gte=price_min)
#             except ValueError:
#                 pass

#         if price_max:
#             try:
#                 price_max = float(price_max)
#                 products = products.filter(price__lte=price_max)
#             except ValueError:
#                 pass

#         if year:
#             try:
#                 year = int(year)
#                 products = products.filter(year=year)
#             except ValueError:
#                 pass
#         if category:
#             products = products.filter(category__icontains=category)
#         # if price_min:
#         #     products = products.filter(price__gte=price_min)
#         # if price_max:
#         #     products = products.filter(price__lte=price_max)
#         # if year:
#         #     products = products.filter(year=year)
#         if brand:
#             products = products.filter(brand__icontains=brand)
#         if area:
#             products = products.filter(area__icontains=area)
#          # Debugging: Print the number of products after applying filters
#         print(f"Number of products after filtering: {len(products)}")

#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)

# # User registration view
# class RegisterView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         email = request.data.get('email')

#         if not username or not password or not email:
#             return Response({"message": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

#         # Create user logic here
#         try:
#             user = User.objects.create_user(username=username, password=password, email=email)
#             user.save()
#             return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# # User login view
# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({
#                 'message': 'Login successful!',
#                 'token': token.key
#             }, status=status.HTTP_200_OK)
#         return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)




# class ProductCreateView(APIView):
#     permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

#     def post(self, request):
#         # Get product data from the request
#         data = request.data
#         data['created_by'] = request.user.id  # Associate the product with the logged-in user
        
#         # Serialize the product data
#         serializer = ProductSerializer(data=data)

#         # Check if data is valid and create product
#         if serializer.is_valid():
#             serializer.save()  # Save the product instance
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        
#         # If data is not valid, return error response
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# # react code starts from here

# #AddProduct.jsx

# import React, { useState } from 'react';
# import axios from 'axios';

# const AddProduct = () => {
#     const [name, setName] = useState('');
#     const [description, setDescription] = useState('');
#     const [price, setPrice] = useState('');
#     const [brand, setBrand] = useState('');
#     const [category, setCategory] = useState('');
#     const [year, setYear] = useState('');
#     const [area, setArea] = useState('');
#     const [message, setMessage] = useState('');

#     const handleSubmit = async (e) => {
#         e.preventDefault();

#         // Get the token from localStorage to authenticate the user
#         const token = localStorage.getItem('token');

#         if (!token) {
#             setMessage('You must be logged in to post a product');
#             return;
#         }

#         try {
#             const response = await axios.post(
#                 'http://localhost:8000/api/products/create/', 
#                 {
#                     name,
#                     description,
#                     price,
#                     brand,
#                     category,
#                     year,
#                     area
#                 },
#                 {
#                     headers: {
#                         Authorization: `Bearer ${token}`,
#                     },
#                 }
#             );
#             setMessage('Product added successfully!');
#         } catch (error) {
#             setMessage('Error: ' + error.response?.data?.detail || 'Something went wrong');
#         }
#     };

#     return (
#         <div>
#             <h2>Add New Product</h2>
#             <form onSubmit={handleSubmit}>
#                 <input 
#                     type="text" 
#                     placeholder="Name" 
#                     value={name} 
#                     onChange={(e) => setName(e.target.value)} 
#                 />
#                 <textarea 
#                     placeholder="Description" 
#                     value={description} 
#                     onChange={(e) => setDescription(e.target.value)} 
#                 />
#                 <input 
#                     type="number" 
#                     placeholder="Price" 
#                     value={price} 
#                     onChange={(e) => setPrice(e.target.value)} 
#                 />
#                 <input 
#                     type="text" 
#                     placeholder="Brand" 
#                     value={brand} 
#                     onChange={(e) => setBrand(e.target.value)} 
#                 />
#                 <input 
#                     type="text" 
#                     placeholder="Category" 
#                     value={category} 
#                     onChange={(e) => setCategory(e.target.value)} 
#                 />
#                 <input 
#                     type="number" 
#                     placeholder="Year" 
#                     value={year} 
#                     onChange={(e) => setYear(e.target.value)} 
#                 />
#                 <input 
#                     type="text" 
#                     placeholder="Area" 
#                     value={area} 
#                     onChange={(e) => setArea(e.target.value)} 
#                 />
#                 <button type="submit">Add Product</button>
#             </form>
#             <div>{message}</div>
#         </div>
#     );
# };

# export default AddProduct;

# #Login.jsx

# import React, { useState } from 'react';
# import axios from 'axios';
# import { useNavigate } from 'react-router-dom'; 

# const Login = () => {    // ---> here now i have passed the
#     const [username, setUsername] = useState('');
#     const [password, setPassword] = useState('');
#     const [message, setMessage] = useState('');
#     const navigate=useNavigate();

#     const handleSubmit = async (e) => {
#         e.preventDefault();
#         try {
#             const response = await axios.post('http://localhost:8000/api/token/', {
#                 username,
#                 password,
#             });
#             localStorage.setItem('token', response.data.access); // Save token in localStorage
#             setMessage('Login successful! now redirecting ...');
#             setTimeout(() => {
#                 navigate('/'); // Use navigate to redirect (this can be '/products' or '/')
#             }, 1000); // Redirect after 1 second
#         } catch (error) {
#             setMessage('Error: ' + error.response.data.detail); // Display the error message
#         }

#     };
#     const handleRegisterClick = () => {
#         navigate('/register'); // Navigate to the Register page
#     };

#     return (
#         <div>
#             <h2>Login</h2>
#             <form onSubmit={handleSubmit}>
#                 <input 
#                     type="text" 
#                     placeholder="Username" 
#                     value={username} 
#                     onChange={(e) => setUsername(e.target.value)} 
#                 /><br></br>
#                 <input 
#                     type="password" 
#                     placeholder="Password" 
#                     value={password} 
#                     onChange={(e) => setPassword(e.target.value)} 
#                 /><br></br>
#                 <button type="submit">Login</button>
#             </form>
#             <div>{message}</div>
#             <h5>Not Registered ? </h5>
#             <button onClick={handleRegisterClick}>Register</button> {/* Button to navigate to Register page */}
#         </div>
#     );
# };

# export default Login;

# #ProductFilters.jsx

# import React, { useState } from 'react';

# const ProductFilter = ({ onFilter }) => {
#     const [priceMin, setPriceMin] = useState();  // ---> the hell man the name here priceMin you need this to
#     const [priceMax, setPriceMax] = useState();  // ---> write in django views to receive the fuck 1 hour wasted
#     const [category, setCategory] = useState('');
#     const [brand, setBrand] = useState('');
#     const [year, setYear] = useState('');

#     const handleFilterSubmit = (e) => {

#     e.preventDefault();

#     // Convert priceMin and priceMax to actual numbers (if they are not empty)
#     const priceMinValue = priceMin ? parseFloat(priceMin) : null;
#     const priceMaxValue = priceMax ? parseFloat(priceMax) : null;
    
#     // Build the filters object
#     const filters = {};

#     if (priceMinValue !== null) filters.priceMin = priceMinValue;
#     if (priceMaxValue !== null) filters.priceMax = priceMaxValue;
#     if (category) filters.category = category;
#     if (brand) filters.brand = brand;
#     if (year) filters.year = year;

#     // Log filters to debug
#     console.log('Filters sent to onFilter:', filters);

#     // Call the onFilter function (assumed to send the data to API)
#     onFilter(filters);
# };
#     return (
#         <form onSubmit={handleFilterSubmit}>
#             <h3>Filtering Options</h3>
            
#                 <label>Price Min:</label>
#                 <input
#                     type="text"
#                     value={priceMin}
#                     onChange={(e) => setPriceMin(e.target.value)}
#                     placeholder="Min Price"
#                 />
            
            
#                 <label>Price Max:</label>
#                 <input
#                     type="text"
#                     value={priceMax}
#                     onChange={(e) => setPriceMax(e.target.value)}
#                     placeholder="Max Price"
#                 />
            
           
#                 <label>Category:</label>
#                 <input
#                     type="text"
#                     value={category}
#                     onChange={(e) => setCategory(e.target.value)}
#                     placeholder="Category"
#                 />
            
          
#                 <label>Brand:</label>
#                 <input
#                     type="text"
#                     value={brand}
#                     onChange={(e) => setBrand(e.target.value)}
#                     placeholder="Brand"
#                 />
           
            
#                 <label>Year:</label>
#                 <input
#                     type="number"
#                     value={year}
#                     onChange={(e) => setYear(e.target.value)}
#                     placeholder="Year"
#                 />
            
#             <button type="submit">Apply Filters</button>
#         </form>
#     );
# };

# export default ProductFilter;

# #ProductList.jsx

# import React, { useEffect, useState } from 'react'; 
# import axios from 'axios';
# import { useNavigate } from 'react-router-dom';

# const ProductList = ({ filters }) => {
#     const [products, setProducts] = useState([]);
#     const [token, setToken] = useState(localStorage.getItem('token')); // Store token in state
#     const navigate = useNavigate();

#     // Effect to fetch products
#     useEffect(() => {
#         let url = 'http://127.0.0.1:8000/api/products/';
        
#         if (filters) {
#             const params = new URLSearchParams(filters);
#             url += `?${params.toString()}`;
#         }

#         // Check if token is available and pass it in the Authorization header if logged in
#         const config = {
#             headers: token ? { Authorization: `Bearer ${token}` } : {}
#         };

#         // Fetch products
#         axios.get(url, config)
#             .then(response => {
#                 setProducts(response.data);
#             })
#             .catch(error => {
#                 console.error('There was an error fetching the products:', error);
#             });
#     }, [filters, token]); // Run effect when filters or token change

#     const handleLoginClick = () => {
#         navigate('/login'); // Redirect to login page
#     };

#     const handleRegisterClick = () => {
#         navigate('/register'); // Redirect to register page
#     };

#     const handleLogoutClick = () => {
#         localStorage.removeItem('token'); // Remove the token from localStorage
#         setToken(null); // Update token state to trigger re-render
#         navigate('/'); // Redirect to home page (or any other page you want)
#     };

#     const handleAddProductClick = () => {
#         if (!token) {
#             alert("You must be logged in to add a product.");
#             navigate('/login'); // Redirect to login page if not logged in
#         } else {
#             navigate('/product-create'); // Redirect to add product page if logged in
#         }
#     };

#     return (
#         <div>
#             <h2>Product List</h2>

#             {token ? (
#                 <>
#                     <button onClick={handleLogoutClick}>Logout</button>
#                 </>
#             ) : (
#                 <>
#                     <button onClick={handleLoginClick}>Login</button>
#                     <button onClick={handleRegisterClick}>Register</button>
#                 </>
#             )}

#             {/* Add Product button always displayed */}
#             <button onClick={handleAddProductClick}>Add Product</button>

#             <ul>
#                 {products.length === 0 ? (
#                     <p>No products available</p> // Display if there are no products
#                 ) : (
#                     products.map((product) => (
#                         <li key={product.id}>
#                             <h3>{product.name}</h3>
#                             <p>{product.description}</p>
#                             <p><strong>Price:</strong> ${product.price}</p>
#                             <p><strong>Brand:</strong> {product.brand}</p>
#                             <p><strong>Category:</strong> {product.category}</p>
#                             <p><strong>Year:</strong> {product.year}</p>
#                             <p><strong>Area:</strong> {product.area}</p>
#                         </li>
#                     ))
#                 )}
#             </ul>
#         </div>
#     );
# };

# export default ProductList;

# #Register.jsx

# import React, { useState } from 'react';
# import axios from 'axios';
# import { useNavigate } from 'react-router-dom'; 

# const Register = () => {
#     const [username, setUsername] = useState('');
#     const [password, setPassword] = useState('');
#     const [email, setEmail] = useState('');
#     const [message, setMessage] = useState('');
#     const navigate=useNavigate();

#     const handleSubmit = async (e) => {
#         e.preventDefault();
#         try {
#             const response = await axios.post('http://localhost:8000/api/register/', {
#                 username,
#                 password,
#                 email,
#             });
#             setMessage(response.data.message);
#             setTimeout(() => {
#                 navigate('/login'); // Use navigate to redirect (this can be '/products' or '/')
#             }, 1000); // Redirect after 1 second
        
#         } catch (error) {
#             setMessage('Error: ' + error.response.data);
#         }
#     };
#     const handleLoginClick = () => {
#         navigate('/login'); // Navigate to the Register page
#     };

#     return (
#         <div>
#             <h2>Register</h2>
#             <form onSubmit={handleSubmit}>
#                 <input 
#                     type="text" 
#                     placeholder="Username" 
#                     value={username} 
#                     onChange={(e) => setUsername(e.target.value)} 
#                 /><br></br>
#                 <input 
#                     type="email" 
#                     placeholder="Email" 
#                     value={email} 
#                     onChange={(e) => setEmail(e.target.value)} 
#                 /><br></br>
#                 <input 
#                     type="password" 
#                     placeholder="Password" 
#                     value={password} 
#                     onChange={(e) => setPassword(e.target.value)} 
#                 /><br></br>
#                 <button type="submit">Register</button>
#             </form>
#             <div>{message}</div>
#             <h5>Already registered ?</h5>
#             <button onClick={handleLoginClick}>Login</button> {/* Button to navigate to Register page */}
#         </div>
#     );
# };

# export default Register;

# #and finally our App.jsx

# import React, { useState, useEffect } from 'react';
# import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
# import Login from './components/Login';
# import Register from './components/Register';
# import ProductList from './components/ProductList';
# import ProductFilter from './components/ProductFilter';
# import AddProduct from './components/AddProduct';

# const App = () => {
#     const [isLoggedIn, setIsLoggedIn] = useState(false);
#     const [showAddProductForm, setShowAddProductForm] = useState(false);
#     const [filters, setFilters] = useState({});
#     useEffect(() => {
#         const token = localStorage.getItem('token');
#         if (token) {
#             setIsLoggedIn(true);
#         } else {
#             setIsLoggedIn(false);
#         }
#     }, []);

#     // Function to toggle product form
#     const handleAddProductToggle = () => {
#         if (!isLoggedIn) {
#             navigate('/login'); // Redirect to login if not logged in
#         } else {
#             setShowAddProductForm(!showAddProductForm);
#         }
#     };

#     const handleFilter = (newFilters) => {
#         setFilters(newFilters);
#     };

#     return (
#         <Router> {/* Ensure the Router is wrapping everything */}
#             <div>
#                 {/* Show the "Add Product" button only if logged in */}
#                 {isLoggedIn && (
#                     <div>
#                         <button onClick={handleAddProductToggle}>
#                             {showAddProductForm ? 'Close Add Product Form' : 'Add New Product'}
#                         </button>
#                     </div>
#                 )}

#                 {/* Conditionally render the add product form */}
#                 {showAddProductForm && <AddProduct />}

#                 <Routes>
#                     <Route path="/login" element={<Login />} />
#                     <Route path="/register" element={<Register />} />
#                     <Route path="/addproduct" element={<AddProduct />} />
#                     <Route path="/" element={
#                         <div>
#                             <ProductFilter onFilter={handleFilter} />
#                             <ProductList filters={filters} />
#                         </div>
#                     } />
#                 </Routes>
#             </div>
#         </Router>
#     );
# };

# export default App;

# # so gpt i want here in my app.jsx should it include only the routes here not logic i think , because when
# # i am logining in the user logs in correctly but i need to refresh the page then the add product button shows
# # the form to add new product and not re redering and after that i also want now for each user to add from the 
# # existing items list which are showing to add the products to there carts 