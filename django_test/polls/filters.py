import django_filters
from django_filters import DateFilter
from .models import *


class OrderFilters(django_filters.FilterSet):
    start_Date = DateFilter(field_name="date_created", lookup_expr='gte')

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['date_created', 'customer']
