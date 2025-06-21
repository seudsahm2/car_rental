from rest_framework import generics
from .models import Car
from .serializers import CarSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class CarListCreateView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'available']
    search_fields = ['title', 'features']
    ordering_fields = ['price', 'year']

class CarRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    

#temporary admin creation view
# from django.contrib.auth.models import User
# from django.http import HttpResponse

# def create_admin(request):
#     if not User.objects.filter(username='adminuser').exists():
#         User.objects.create_superuser('adminuser', 'admin@example.com', 'yourpassword123')
#         return HttpResponse("Admin user created")
#     return HttpResponse("Admin user already exists")
