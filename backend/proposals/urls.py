from django.urls import path
from .views import (
    ProposalListCreateView,
    ProposalRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('', ProposalListCreateView.as_view(),
         name='proposal-list-create'),
    path('<int:pk>/',
         ProposalRetrieveUpdateDestroyView.as_view(), name='proposal-detail'),
]
