import django_tables2 as tables
from .models import Product
from django.utils.html import format_html

class ProductTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name='inventory/includes/actions_column.html',
        orderable=False,
        attrs={"td": {"class": "text-center"}}
    )
    
    class Meta:
        model = Product
        template_name = "django_tables2/bootstrap5.html"
        fields = ('name', 'category', 'sku', 'price', 'quantity', 'status')
        attrs = {
            'class': 'table table-striped table-hover',
            'thead': {
                'class': 'table-dark'
            }
        }
    
    def render_price(self, value):
        return f"${value:.2f}"
    
    def render_status(self, value, record):
        if value == "Out of Stock":
            return format_html('<span class="badge bg-danger">{}</span>', value)
        elif value == "Low Stock":
            return format_html('<span class="badge bg-warning text-dark">{}</span>', value)
        return format_html('<span class="badge bg-success">{}</span>', value)