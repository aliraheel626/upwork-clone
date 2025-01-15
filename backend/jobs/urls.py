from django.urls import path
from .views import JobListCreateView, JobDetailView, ProposalListView, ProposalDetailView

urlpatterns = [
    # Job endpoints
    path('', JobListCreateView.as_view(), name='job-list-create'),
    path('<int:pk>/', JobDetailView.as_view(), name='job-detail'),

    # Proposal endpoints
    path('<int:job_id>/proposals/',
         ProposalListView.as_view(), name='job-proposal-list'),
    path('<int:job_id>/proposals/<int:pk>/',
         ProposalDetailView.as_view(), name='job-proposal-detail'),
]
