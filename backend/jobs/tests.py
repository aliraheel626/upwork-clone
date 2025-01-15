from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Job
from proposals.models import Proposal


class JobProposalAPITest(TestCase):
    def setUp(self):
        # Create users
        self.owner = User.objects.create_user(
            username='owner', password='password123')
        self.other_user = User.objects.create_user(
            username='other_user', password='password123')

        # Create a job associated with the owner
        self.job = Job.objects.create(
            title='Test Job',
            rate=100,
            description='A test job description',
            days_required=5,
            created_at='2025-01-15T12:00:00Z',
            user=self.owner  # Associate the job with the owner
        )

        # Create a proposal for the job by another user
        self.proposal = Proposal.objects.create(
            user=self.other_user,
            description='Test proposal description',
            rate=90,
            days_required=4,
            job=self.job
        )

        # Set up API client
        self.client = APIClient()

    def authenticate_user(self, user):
        self.client.force_authenticate(user=user)

    # Job Tests
    def test_list_jobs(self):
        self.authenticate_user(self.owner)
        url = reverse('job-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Only one job created in setUp
        self.assertEqual(len(response.data), 1)

    def test_retrieve_job(self):
        self.authenticate_user(self.owner)
        url = reverse('job-detail', kwargs={'pk': self.job.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Job')
        # Check owner association
        self.assertEqual(response.data['user'], self.owner.id)

    def test_create_job_authenticated(self):
        self.authenticate_user(self.owner)
        url = reverse('job-list-create')
        data = {
            'title': 'New Job',
            'rate': 120,
            'description': 'Description for new job',
            'days_required': 7
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Job.objects.count(), 2)  # New job created
        # Verify job ownership
        self.assertEqual(Job.objects.last().user, self.owner)

    def test_create_job_unauthenticated(self):
        url = reverse('job-list-create')
        data = {
            'title': 'Unauthorized Job',
            'rate': 150,
            'description': 'Unauthorized job description',
            'days_required': 10
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Proposal Tests
    def test_list_proposals(self):
        url = reverse('job-proposal-list', kwargs={'job_id': self.job.id})
        self.authenticate_user(self.owner)  # Owner of the job
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # One proposal created in setUp
        self.assertEqual(len(response.data), 1)

    def test_retrieve_proposal(self):
        url = reverse('job-proposal-detail',
                      kwargs={'job_id': self.job.id, 'pk': self.proposal.id})
        self.authenticate_user(self.owner)  # Owner of the job
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['description'], 'Test proposal description')

    def test_list_proposals_unauthorized(self):
        url = reverse('job-proposal-list', kwargs={'job_id': self.job.id})
        response = self.client.get(url)  # Unauthenticated request
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_proposals_not_owner(self):
        self.authenticate_user(self.other_user)  # Not the owner of the job
        url = reverse('job-proposal-list', kwargs={'job_id': self.job.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
