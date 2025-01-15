from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        contract_id = self.kwargs['contract_id']
        return Review.objects.filter(contract_id=contract_id)

    def perform_create(self, serializer):
        contract_id = self.kwargs['contract_id']
        serializer.save(contract_id=contract_id)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        contract_id = self.kwargs['contract_id']
        return Review.objects.filter(contract_id=contract_id)
