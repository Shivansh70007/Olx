import os
import django
from datetime import datetime

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Olx.settings") #--> your project name 
django.setup()

# Import the Product model
                                                                                                                                                             
# from products.model import Product

def populate_db():
    # Sample products data
    products_data = [
        {
            "name": "iPhone 13",
            "description": "Apple iPhone 13 with 128GB storage, A15 Bionic chip, and 5G capability.",
            "price": 799.99,
            "brand": "Apple",
            "category": "Smartphones",
            "year": 2021,
            "area": "New York",
            "created_at": datetime(2024, 12, 26, 10, 0, 0)
        },
        {
            "name": "Samsung Galaxy S21",
            "description": "Samsung Galaxy S21 with 256GB storage, Exynos 2100 chipset, and AMOLED display.",
            "price": 999.99,
            "brand": "Samsung",
            "category": "Smartphones",
            "year": 2021,
            "area": "Los Angeles",
            "created_at": datetime(2024, 12, 26, 10, 0, 0)
        },
        {
            "name": "MacBook Air M1",
            "description": "Apple MacBook Air powered by M1 chip with 8GB RAM and 256GB SSD.",
            "price": 999.99,
            "brand": "Apple",
            "category": "Laptops",
            "year": 2020,
            "area": "San Francisco",
            "created_at": datetime(2024, 12, 26, 10, 0, 0)
        },
        {
            "name": "Sony WH-1000XM4",
            "description": "Sony noise-canceling headphones with exceptional sound quality and long battery life.",
            "price": 348.00,
            "brand": "Sony",
            "category": "Headphones",
            "year": 2020,
            "area": "Chicago",
            "created_at": datetime(2024, 12, 26, 10, 0, 0)
        },
        {
            "name": "Dell XPS 13",
            "description": "Dell XPS 13 with Intel Core i7, 16GB RAM, and 512GB SSD.",
            "price": 1399.99,
            "brand": "Dell",
            "category": "Laptops",
            "year": 2021,
            "area": "Seattle",
            "created_at": datetime(2024, 12, 26, 10, 0, 0)
        },
        {
            "name": "Nintendo Switch",
            "description": "Nintendo Switch with neon blue and red joy-cons, perfect for gaming on the go.",
            "price": 299.99,
            "brand": "Nintendo",
            "category": "Gaming Consoles",
            "year": 2021,
            "area": "Austin",
            "created_at": datetime(2024, 12, 26, 10, 0, 0)
        },
        {
            "name": "Google Pixel 6",
            "description": "Google Pixel 6 with 128GB storage, Google Tensor chip, and high-quality camera.",
            "price": 599.99,
            "brand": "Google",
            "category": "Smartphones",
            "year": 2021,
            "area": "Houston",
            "created_at": datetime(2024, 12, 26, 10, 0, 0)
        },
        {
            "name": "Bose QuietComfort 35 II",
            "description": "Bose over-ear wireless noise-canceling headphones with great sound and comfort.",
            "price": 299.99,
            "brand": "Bose",
            "category": "Headphones",
            "year": 2019,
            "area": "Miami",
            "created_at": datetime(2024, 12, 26, 10, 0, 0)
        },
        {
            "name": "Apple Watch Series 7",
            "description": "Apple Watch Series 7 with a larger display, fast charging, and fitness tracking.",
            "price": 399.99,
            "brand": "Apple",
            "category": "Wearables",
            "year": 2021,
            "area": "Denver",
            "created_at": datetime(2024, 12, 26, 10, 0, 0)
        },
        {
            "name": "Fitbit Charge 5",
            "description": "Fitbit Charge 5 with built-in GPS, heart rate monitor, and sleep tracking.",
            "price": 179.95,
            "brand": "Fitbit",
            "category": "Wearables",
            "year": 2021,
            "area": "Phoenix",
            "created_at": datetime(2024, 12, 26, 10, 0, 0)
        }
    ]

    # Loop through the data and create Product objects
    for product_data in products_data:
        product = Product(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            brand=product_data['brand'],
            category=product_data['category'],
            year=product_data['year'],
            area=product_data['area'],
            created_at=product_data['created_at']
        )
        product.save()
        print(f"Product '{product.name}' added to the database.")

# Call the populate_db function to insert data into the database
populate_db()