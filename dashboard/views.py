from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.urls import reverse
from django.urls import reverse_lazy
from inventory.models import Product, Category

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list_url'] = reverse_lazy('inventory:product-list')
        context['category_list_url'] = reverse_lazy('inventory:category-list') 
        
        # Basic counts
        context['total_products'] = Product.objects.count()
        context['total_categories'] = Category.objects.count()
        
        # Low stock alerts (assuming you have a reorder_level field)
        context['low_stock_products'] = Product.objects.filter(
            quantity__lte=models.F('reorder_level')
        ).exclude(quantity=0).count()
        
        # Recent products
        context['recent_products'] = Product.objects.order_by('-created_at')[:5]
        
        # Out of stock items
        context['out_of_stock'] = Product.objects.filter(quantity=0).count()
        
        return context