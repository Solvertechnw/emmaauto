from rest_framework import viewsets, filters
from cars.models import Car
from .serializers import CarSerializer

class CarViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Car.objects.all().order_by('-created')
    serializer_class = CarSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title','description','make','model']
