from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('customers/', views.customer_overview, name='customer_overview'),
    path('products/', views.product_overview, name='product_overview'),
    path('orders/<int:customer_id>/', views.order_details, name='order_details'),
    path('customers_with_orders/', views.customers_with_orders, name='customers_with_orders'),
    path('customer_revenue/', views.customer_revenue, name='customer_revenue'),
    path('best_selling_products/', views.best_selling_products, name='best_selling_products'),
    path('high_spending_customers/', views.high_spending_customers, name='high_spending_customers'),
    path('questions/', views.questions, name='questions'),
    path('questions/<str:section>/', views.questions_detail, name='questions_detail'),
]
