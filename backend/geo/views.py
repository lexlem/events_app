from rest_framework import mixins, generics, status

from .models import City
from .serializers import CitySerializer


class CityList(
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    queryset = City.objects.filter(
        importance_index__gte=2).order_by("-importance_index", "raw")
    serializer_class = CitySerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
