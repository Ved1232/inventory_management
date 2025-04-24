
from django.urls import path
from .views import ProductListView
from .views import (CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, 
                    ProductListView, ProductCreateView, ProductDetailView, ProductUpdateView, 
                    ProductDeleteView, )


app_name = 'inventory'
urlpatterns = [
    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/add/', CategoryCreateView.as_view(), name='category-add'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category-edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    
    # Product URLs
    path('products/', ProductListView.as_view(), name='products'),
    path('products/add/', ProductCreateView.as_view(), name='product-add'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product-edit'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
]
