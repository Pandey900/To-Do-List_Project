from django.test import TestCase
from django.contrib.auth.models import User
from .models import Task
from django.urls import reverse


class TaskTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.task = Task.objects.create(
            user=self.user, title="Test Task", description="This is a test task", complete=False
        )

    def test_user_registration(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "password1": "newpass123",
            "password2": "newpass123"
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_user_login(self):
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "testpass123"
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_task_creation(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(reverse("task-create"), {
            "title": "New Task",
            "description": "New task description",
            "complete": False,
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Task.objects.filter(title="New Task").exists())

    def test_task_update(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("task-update", args=[self.task.id]),
            {"title": "Updated Task", "description": "Updated description", "complete": True},
        )
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")
        self.assertTrue(self.task.complete)

    def test_task_deletion(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(reverse("task-delete", args=[self.task.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
