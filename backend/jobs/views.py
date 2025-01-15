from proposals.serializers import ProposalSerializer
from proposals.models import Proposal
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Job
from .serializers import JobSerializer
from rest_framework.permissions import BasePermission

# List all jobs or create a new job


class IsOwner(BasePermission):
    """
    Custom permission to check if the user is the owner of the job.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the job associated with the proposal

        return obj.user == request.user


class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically assign the authenticated user as the owner
        serializer.save(user=self.request.user)

# Retrieve, update, or delete a specific job


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]


# List all proposals for a specific job or create a new proposal


class ProposalListView(generics.ListAPIView):
    """
    List all proposals for a specific job (read-only),
    ensuring the user is the owner of the job.
    """
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        job = Job.objects.filter(id=job_id).first()
        self.check_object_permissions(self.request, job)
        return Proposal.objects.filter(job_id=job_id)

    # def get_object(self):
    #     print('call')
    #     # Ensure the user is the owner of the job
    #     queryset = self.get_queryset()
    #     obj = queryset.first()
    #     self.check_object_permissions(self.request, obj)
    #     return obj


class ProposalDetailView(generics.RetrieveAPIView):
    """
    Retrieve a specific proposal (read-only),
    ensuring the user is the owner of the job.
    """
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_object(self):

        # Ensure the user is the owner of the job associated with the proposal
        # obj = super().get_object()
        job_id = self.kwargs['job_id']
        job = Job.objects.filter(id=job_id).first()
        print(type(job))

        self.check_object_permissions(self.request, job)
        proposal = Proposal.objects.filter(id=self.kwargs['pk']).first()
        return proposal
