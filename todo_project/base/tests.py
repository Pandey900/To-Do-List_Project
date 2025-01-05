from django.test import TestCase
from django.contrib.auth.models import User
from .models import Task
from django.urls import reverse


class TaskTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.task = Task.objects.create(
            user=self.user, title="Test Task", description="This is a test task", complete=False
        )

    def test_task_creation(self):
        # Verify the task was created
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.description, "This is a test task")
        self.assertFalse(self.task.complete)
        self.assertEqual(self.task.user, self.user)

    def test_task_list_view(self):
        # Login the test user
        self.client.login(username="testuser", password="testpass123")

        # Fetch the task list
        response = self.client.get(reverse("tasks"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")
        self.assertEqual(len(response.context["tasks"]), 1)

    def test_task_update(self):
        # Login the test user
        self.client.login(username="testuser", password="testpass123")

        # Update the task
        response = self.client.post(
            reverse("task-update", args=[self.task.id]),
            {"title": "Updated Task", "description": "Updated description", "complete": True},
        )

        # Reload the task from the database
        self.task.refresh_from_db()

        # Verify the task was updated
        self.assertEqual(self.task.title, "Updated Task")
        self.assertEqual(self.task.description, "Updated description")
        self.assertTrue(self.task.complete)
