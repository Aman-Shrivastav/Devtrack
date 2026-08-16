from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Workspace, WorkspaceMember


class AtomicWorkspaceCreationTests(APITestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner = user_model.objects.create_user(
            username='owner', password='safe-password'
        )
        self.member = user_model.objects.create_user(
            username='member', password='safe-password'
        )
        self.client.force_authenticate(self.owner)

    def test_duplicate_member_rolls_back_workspace_and_memberships(self):
        response = self.client.post(
            '/api/workspaces/atomic-create/',
            {
                'name': 'Rollback demo',
                'description': 'This request must not persist any data.',
                'members': [
                    {'user': str(self.member.id), 'role': 'EDITOR'},
                    {'user': str(self.member.id), 'role': 'VIEWER'},
                ],
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(Workspace.objects.count(), 0)
        self.assertEqual(WorkspaceMember.objects.count(), 0)
