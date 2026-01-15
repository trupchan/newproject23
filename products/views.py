from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Product
from .serializers import ProductSerializer
from .permissions import IsModerator


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            # модератору POST запрещён
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsModerator()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

