from .views import ReviewListCreateView, ReviewDetailView
from django.urls import path
urlpatterns = [
    # List all reviews for a contract or create a new review
    path('contracts/<int:contract_id>/reviews/',
         ReviewListCreateView.as_view(), name='review-list-create'),

    # Retrieve, update, or delete a specific review
    path('contracts/<int:contract_id>/reviews/<int:pk>/',
         ReviewDetailView.as_view(), name='review-detail'),
]
