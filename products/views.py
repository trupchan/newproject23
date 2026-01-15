from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Product
from .serializers import ProductSerializer
from .permissions import IsModerator
from common.validators import validate_user_age_from_token

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsModerator()]

    def perform_create(self, serializer):
        validate_user_age_from_token(self.request)
        serializer.save(owner=self.request.user)
