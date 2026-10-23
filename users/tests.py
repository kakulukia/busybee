from django.test import TestCase, override_settings
from post_office.models import Email, EmailTemplate, STATUS

from users.models import User


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class LoginTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.data.create_user(
            username="admin-test", password="test-password", is_staff=True
        )

    def test_staff_can_log_in(self):
        response = self.client.post(
            "/admin/login/",
            {
                "username": self.user.username,
                "password": "test-password",
                "next": "/admin/",
            },
        )
        self.assertRedirects(response, "/admin/")

    def test_lockout_blocks_correct_password_but_keeps_ip_combinations_separate(self):
        credentials = {
            "username": self.user.username,
            "password": "incorrect",
            "next": "/admin/",
        }
        self.assertEqual(self.client.post("/admin/login/", credentials).status_code, 200)
        self.assertEqual(self.client.post("/admin/login/", credentials).status_code, 429)
        credentials["password"] = "test-password"
        self.assertEqual(self.client.post("/admin/login/", credentials).status_code, 429)
        response = self.client.post("/admin/login/", credentials, REMOTE_ADDR="127.0.0.2")
        self.assertRedirects(response, "/admin/")

    def test_regular_user_cannot_log_in_to_admin(self):
        self.user.is_staff = False
        self.user.save()
        response = self.client.post(
            "/admin/login/",
            {
                "username": self.user.username,
                "password": "test-password",
                "next": "/admin/",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)


class EmailTests(TestCase):
    def test_template_email_is_queued(self):
        template = EmailTemplate.objects.create(
            name="kontakt", subject="Contact", content="{{ content.message }}"
        )
        user = User.data.create_user(username="EMAIL", email="recipient@example.com")
        user.email_user("kontakt", {"content": {"message": "Test message"}})
        email = Email.objects.get()
        self.assertEqual(email.to, ["recipient@example.com"])
        self.assertEqual(email.template, template)
        self.assertEqual(email.status, STATUS.queued)
