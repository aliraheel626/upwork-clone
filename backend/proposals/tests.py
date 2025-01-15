from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from jobs.models import Job
from .models import Proposal


class ProposalAPITestCase(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(
            username="user1", password="password1")
        self.user2 = User.objects.create_user(
            username="user2", password="password2")

        # Create a job
        self.job = Job.objects.create(
            title="Test Job", description="Job Description")

        # Create proposals
        self.proposal1 = Proposal.objects.create(
            user=self.user1, description="Proposal 1", rate=100.00, job=self.job
        )
        self.proposal2 = Proposal.objects.create(
            user=self.user2, description="Proposal 2", rate=200.00, job=self.job
        )

        # API client
        self.client = APIClient()

    def authenticate(self, user):
        """Helper method to authenticate a user."""
        self.client.force_authenticate(user=user)

    def test_list_proposals(self):
        """Test listing all proposals."""
        self.authenticate(self.user1)
        response = self.client.get(reverse('proposal-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_proposal(self):
        """Test creating a new proposal."""
        # Create a new job to avoid conflicts
        new_job = Job.objects.create(
            title="New Job", description="Another Job Description")
        self.authenticate(self.user1)  # Authenticate as user1
        payload = {
            "description": "New Proposal",
            "rate": 150.00,
            "job": new_job.id,
        }
        response = self.client.post(reverse('proposal-list-create'), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Ensure proposal is created for new job
        self.assertEqual(Proposal.objects.filter(job=new_job).count(), 1)
        self.assertEqual(response.data["description"], "New Proposal")

    def test_retrieve_proposal(self):
        """Test retrieving a specific proposal."""
        self.authenticate(self.user1)
        response = self.client.get(
            reverse('proposal-detail', args=[self.proposal1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["description"], self.proposal1.description)

    def test_update_proposal(self):
        """Test updating a proposal."""
        self.authenticate(self.user1)
        payload = {
            "description": "Updated Proposal 1",
            "rate": 120.00,
            "job": self.job.id,
        }
        response = self.client.put(
            reverse('proposal-detail', args=[self.proposal1.id]), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.proposal1.refresh_from_db()
        self.assertEqual(self.proposal1.description, "Updated Proposal 1")
        self.assertEqual(self.proposal1.rate, 120.00)

    def test_delete_proposal(self):
        """Test deleting a proposal."""
        self.authenticate(self.user1)
        response = self.client.delete(
            reverse('proposal-detail', args=[self.proposal1.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Proposal.objects.filter(
            id=self.proposal1.id).exists())

    def test_retrieve_proposal_permission_denied(self):
        """Test that a user cannot retrieve another user's proposal."""
        self.authenticate(self.user2)
        response = self.client.get(
            reverse('proposal-detail', args=[self.proposal1.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_proposal_permission_denied(self):
        """Test that a user cannot update another user's proposal."""
        self.authenticate(self.user2)
        payload = {
            "description": "Hacked Proposal",
            "rate": 500.00,
            "job": self.job.id,
        }
        response = self.client.put(
            reverse('proposal-detail', args=[self.proposal1.id]), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_proposal_permission_denied(self):
        """Test that a user cannot delete another user's proposal."""
        self.authenticate(self.user2)
        response = self.client.delete(
            reverse('proposal-detail', args=[self.proposal1.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_proposal_duplicate(self):
        """Test that a user cannot create multiple proposals for the same job."""
        self.authenticate(self.user1)  # Authenticate as user1
        payload = {
            "description": "Duplicate Proposal",
            "rate": 150.00,
            "job": self.job.id,
        }
        response = self.client.post(reverse('proposal-list-create'), payload)

        # Assert that the response status code is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that the error message is appropriate
        self.assertIn("detail", response.data)
        # self.assertEqual(
        #     response.data["detail"], "Proposal with this user and job already exists.")
