from io import BytesIO
import re
from unittest.mock import patch

from django.test import SimpleTestCase, TestCase
from PIL import Image

import fabfile
from bee.models import EmailLog
from users.models import User


class PageTests(TestCase):
    def test_public_pages_render(self):
        paths = (
            "/",
            "/kontakt",
            "/kontakt-danke",
            "/busy-bee-world",
            "/jetzt-anfragen",
            "/jetzt-anfragen-danke",
            "/datenschutz",
            "/impressum",
            "/agb",
            "/buffet-menue",
            "/fingerfood",
            "/inspiration",
            "/bio-und-allergene-welt",
            "/full-service",
            "/getraenke",
            "/office-lunch",
            "/event-consulting",
            "/admin/login/",
        )
        for path in paths:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_contact_captcha_image_is_valid(self):
        response = self.client.get("/kontakt")
        image_url = re.search(r'src="(/captcha/image/[^"]+)"', response.content.decode())
        self.assertIsNotNone(image_url)
        image_response = self.client.get(image_url.group(1))
        self.assertEqual(image_response.status_code, 200)
        self.assertEqual(image_response["Content-Type"], "image/png")
        Image.open(BytesIO(image_response.content)).verify()


class DeploymentTests(SimpleTestCase):
    @patch("fabfile.run")
    def test_migrate_uses_locked_production_dependencies(self, run):
        fabfile.migrate()
        self.assertEqual(
            [call.args[0] for call in run.call_args_list],
            [
                "git pull",
                "uv sync --locked --no-dev",
                "uv run --locked --no-dev python manage.py migrate --noinput",
                "uv run --locked --no-dev python manage.py compress -e pug,html --force",
                "uv run --locked --no-dev python manage.py collectstatic --noinput",
                "pm2 restart busybee",
                "uv run --locked --no-dev python manage.py clear_cache",
            ],
        )


@patch("captcha.conf.settings.CAPTCHA_TEST_MODE", True)
class FormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.data.create_user(username="EMAIL", email="recipient@example.com")

    @patch("bee.views.User.email_user")
    def test_empty_contact_shows_required_field_errors(self, send_mail):
        response = self.client.post("/kontakt", {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            set(response.context["form"].errors), {"name", "email", "message", "captcha"}
        )
        send_mail.assert_not_called()

    @patch("bee.views.User.email_user")
    def test_incomplete_contact_with_link_shows_field_errors(self, send_mail):
        response = self.client.post(
            "/kontakt", {"email": "invalid", "message": "https://example.com"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.context["form"].errors)
        self.assertIn("email", response.context["form"].errors)
        self.assertFalse(EmailLog.data.exists())
        send_mail.assert_not_called()

    @patch("bee.views.User.email_user")
    def test_valid_contact_still_sends(self, send_mail):
        response = self.client.post(
            "/kontakt",
            {
                "name": "Test",
                "email": "sender@example.com",
                "message": "Test message",
                "captcha_0": "test",
                "captcha_1": "PASSED",
            },
        )
        self.assertRedirects(response, "/kontakt-danke")
        send_mail.assert_called_once_with(
            "kontakt",
            {
                "content": {
                    "Name": "Test",
                    "E-Mail": "sender@example.com",
                    "Nachricht": "Test message",
                }
            },
        )

    @patch("bee.views.User.email_user")
    def test_contact_spam_is_still_logged_and_rejected(self, send_mail):
        response = self.client.post(
            "/kontakt",
            {
                "name": "Test",
                "email": "sender@example.com",
                "message": "https://example.com",
                "captcha_0": "test",
                "captcha_1": "PASSED",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].non_field_errors())
        self.assertEqual(EmailLog.data.get().message, "https://example.com")
        send_mail.assert_not_called()

    @patch("bee.views.User.email_user")
    def test_incorrect_captcha_prevents_contact_email(self, send_mail):
        response = self.client.post(
            "/kontakt",
            {
                "name": "Test",
                "email": "sender@example.com",
                "message": "Test message",
                "captcha_0": "test",
                "captcha_1": "incorrect",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("captcha", response.context["form"].errors)
        send_mail.assert_not_called()

    @patch("bee.views.User.email_user")
    def test_invalid_requests_are_rejected_without_sending(self, send_mail):
        payloads = (
            {},
            {"form-nonce": "100"},
            {"form-nonce": "100", "data[name]": "   "},
            {"data[name]": "Test"},
            {"form-nonce": "invalid", "data[name]": "Test"},
            {"form-nonce": "100", "data[anrede]": "999"},
        )
        for payload in payloads:
            with self.subTest(payload=payload):
                response = self.client.post("/jetzt-anfragen", payload)
                self.assertContains(response, "Bitte", status_code=400)
        send_mail.assert_not_called()

    @patch("bee.views.User.email_user")
    @patch("bee.views.time", return_value=200)
    def test_valid_request_keeps_option_mapping_and_spam_detection(self, now, send_mail):
        for start, spam in (("100", ""), ("190", "(SPAM?)")):
            with self.subTest(start=start):
                send_mail.reset_mock()
                response = self.client.post(
                    "/jetzt-anfragen",
                    {"form-nonce": start, "data[name]": "Test", "data[anrede]": "1"},
                )
                self.assertRedirects(response, "/jetzt-anfragen-danke")
                send_mail.assert_called_once_with(
                    "anfrage",
                    {"content": {"Name": "Test", "Anrede": "Frau"}, "spam": spam},
                )
