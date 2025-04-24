from django.db import models 
from django.urls import reverse_lazy 
from django.views.generic import (ListView, CreateView, UpdateView, 
                                 DeleteView, DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django_tables2 import SingleTableView
from . import models
from .models import Category, Product
from .forms import CategoryForm, ProductForm
from .tables import ProductTable
from .filters import ProductFilter
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
# Category Views
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'inventory/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'inventory/category_form.html'
    success_url = reverse_lazy('inventory:category-list')
    success_message = "Category was created successfully!"

class CategoryUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'inventory/category_form.html'
    success_url = reverse_lazy('inventory:category-list')
    success_message = "Category was updated successfully!"

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'inventory/category_confirm_delete.html'
    success_url = reverse_lazy('inventory:category-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Category was deleted successfully!")
        return super().delete(request, *args, **kwargs)

# Product Views
class ProductListView(LoginRequiredMixin, SingleTableView):
    model = Product
    table_class = ProductTable
    template_name = 'inventory/product_list.html'
    filterset_class = ProductFilter
    paginate_by = 25  # Added pagination
    
    def get_queryset(self):
        try:
            queryset = super().get_queryset()\
                .select_related('category')\
                .order_by('-created_at')  # Default ordering
            
            self.filterset = self.filterset_class(
                self.request.GET, 
                queryset=queryset,
                request=self.request
            )
            
            if not self.filterset.is_valid():
                messages.error(self.request, "Invalid filter parameters")
                return queryset.none()
                
            return self.filterset.qs.distinct()
            
        except Exception as e:
            messages.error(self.request, f"Error loading products: {str(e)}")
            return Product.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['export_url'] = reverse_lazy('inventory:product-export')
        
        # Add category list URL to context to fix the NoReverseMatch error
        context['category_list_url'] = reverse_lazy('inventory:category-list')
        
        # Add stats
        context['total_products'] = self.model.objects.count()
        context['low_stock_count'] = self.model.objects.filter(
            quantity__lte=models.F('reorder_level'),
            quantity__gt=0
        ).count()
        
        return context
    
    def get_table_kwargs(self):
        return {
            'request': self.request,
            'empty_text': 'No products found matching your criteria'
        }

class ProductCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('inventory:products')
    success_message = "Product was created successfully!"

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'inventory/product_detail.html'

class ProductUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('inventory:products')
    success_message = "Product was updated successfully!"

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'inventory/product_confirm_delete.html'
    success_url = reverse_lazy('inventory:products')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Product was deleted successfully!")
        return super().delete(request, *args, **kwargs)