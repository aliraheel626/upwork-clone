from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Proposal
from backend.permissions import IsOwner
from .serializers import ProposalSerializer


from rest_framework.exceptions import ValidationError
from django.db import IntegrityError

from rest_framework.permissions import BasePermission


# from django.urls import path
# from .views import (
#     ProposalListCreateView,
#     ProposalRetrieveUpdateDestroyView,
# )

# urlpatterns = [
#     path('', ProposalListCreateView.as_view(),
#          name='proposal-list-create'),
#     path('<int:pk>/',
#          ProposalRetrieveUpdateDestroyView.as_view(), name='proposal-detail'),
# ]


class ProposalListCreateView(generics.ListCreateAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            # Automatically assign the logged-in user as the proposal owner
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError(
                {"detail": "You have already submitted a proposal for this job."})


# Retrieve, Update, or Delete a Specific Proposal
class ProposalRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated, IsOwner]
