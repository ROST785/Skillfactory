from django_filters import FilterSet
from .models import Response


class ResponsesFilter(FilterSet):
    class Meta:
        model = Response
        fields = {
            'announcement__name': ['icontains']
        }
