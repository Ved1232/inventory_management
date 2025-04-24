import django_filters
from .models import Product 
from django.db.models import F

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name contains')
    sku = django_filters.CharFilter(lookup_expr='icontains', label='SKU contains')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Min price')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Max price')
    min_quantity = django_filters.NumberFilter(field_name='quantity', lookup_expr='gte', label='Min quantity')
    max_quantity = django_filters.NumberFilter(field_name='quantity', lookup_expr='lte', label='Max quantity')
    
    STATUS_CHOICES = [
        ('in_stock', 'In Stock'),
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out of Stock'),
    ]
    
    status = django_filters.ChoiceFilter(
        choices=STATUS_CHOICES,
        method='filter_by_status',
        label='Status'
    )
    
    class Meta:
        model = Product
        fields = ['category']
    
    def filter_by_status(self, queryset, name, value):
        if value == 'in_stock':
            return queryset.filter(quantity__gt=F('reorder_level'))
        elif value == 'low_stock':
            return queryset.filter(quantity__lte=F('reorder_level'), quantity__gt=0)
        elif value == 'out_of_stock':
            return queryset.filter(quantity=0)
        return queryset