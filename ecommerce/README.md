# E-Commerce Django Application

This is a simple E-Commerce application developed using Django. The application consists of a MySQL database to store customer, product, and order data, and a dynamic frontend to display this data.

## Project Overview

The goal of this project was to create a small database that stores basic information about products, orders, and customers, and then display this data dynamically through a Django-based frontend.

### Features Implemented:

1. **Database Design:**
   - A schema for a simple E-Commerce database with the following tables:
     - `customers` - Stores customer information such as name, email, address, and phone number.
     - `products` - Stores product details such as name, description, price, category, and inventory.
     - `orders` - Stores order information, including the customer who placed the order and the date of the order.
     - `order_items` - Stores the items included in each order, linking products to orders with quantity and price.

2. **Data Insertion:**
   - Sample data has been inserted into each table to demonstrate functionality.

3. **SQL Queries:**
   - The application includes SQL queries to retrieve the following information:
     1. **Customers with Orders:** The names of all customers who have placed at least one order.
     2. **Customer Revenue:** The total number of orders and total revenue for each customer.
     3. **Best-Selling Products:** The most popular products based on the number of orders.
     4. **High-Spending Customers:** A list of customers who have spent more than 500 Euros.

4. **Frontend:**
   - Django views and templates were implemented to provide the following pages:
     - **Customer Overview:** Displays all customers with their names, email addresses, and the number of orders placed.
     - **Order Details:** Shows the details of the orders placed by a selected customer, including the ordered products and the total amount.
     - **Product Overview:** Lists all products with their name, description, and price.
     - **Best-Selling Products:** Displays the most popular products based on order count and quantity ordered.
     - **High-Spending Customers:** Displays customers who have spent more than 500 Euros on their orders.

## Setup Instructions

### Prerequisites

- **Python 3.12.4**
- **Django 5.0.7**
- **MySQL**

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/devgirlpro/ecommerce-django.git
   cd ecommerce-django

   2. Create and Activate a Virtual Environment

   3. nstall the Dependencies

   4. Set Up the MySQL Database: 
   **sql
        CREATE DATABASE ecommerce_db;

Create a MySQL user
CREATE USER root@'localhost' IDENTIFIED BY AzadehGalidari1992;
GRANT ALL PRIVILEGES ON ecommerce_db.* TO root@'localhost';
FLUSH PRIVILEGES;

5. Configure Database Settings:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce_db',
        'USER': 'root',
        'PASSWORD': 'AzadehGalidari1992',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

6. Apply the Database Migrations

7. Create a Superuser 
name: root
password: root

8.Run the Development Server

Usage
Admin Panel: Access the Django admin panel at http://127.0.0.1:8000/admin/
Customer Overview: View customer details at http://127.0.0.1:8000/customers/
Product Overview: View product details at http://127.0.0.1:8000/products/
Order Details: View order details by navigating to http://127.0.0.1:8000/orders/<customer_id>/