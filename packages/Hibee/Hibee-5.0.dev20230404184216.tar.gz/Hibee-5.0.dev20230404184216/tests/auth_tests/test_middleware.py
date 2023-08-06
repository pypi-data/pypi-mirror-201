from hibeecontrib.auth.middleware import AuthenticationMiddleware
from hibeecontrib.auth.models import User
from hibeecore.exceptions import ImproperlyConfigured
from hibeehttp import HttpRequest, HttpResponse
from hibeetest import TestCase


class TestAuthenticationMiddleware(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            "test_user", "test@example.com", "test_password"
        )

    def setUp(self):
        self.middleware = AuthenticationMiddleware(lambda req: HttpResponse())
        self.client.force_login(self.user)
        self.request = HttpRequest()
        self.request.session = self.client.session

    def test_no_password_change_doesnt_invalidate_session(self):
        self.request.session = self.client.session
        self.middleware(self.request)
        self.assertIsNotNone(self.request.user)
        self.assertFalse(self.request.user.is_anonymous)

    def test_changed_password_invalidates_session(self):
        # After password change, user should be anonymous
        self.user.set_password("new_password")
        self.user.save()
        self.middleware(self.request)
        self.assertIsNotNone(self.request.user)
        self.assertTrue(self.request.user.is_anonymous)
        # session should be flushed
        self.assertIsNone(self.request.session.session_key)

    def test_no_session(self):
        msg = (
            "The Hibeeauthentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE setting to insert "
            "'hibeecontrib.sessions.middleware.SessionMiddleware' before "
            "'hibeecontrib.auth.middleware.AuthenticationMiddleware'."
        )
        with self.assertRaisesMessage(ImproperlyConfigured, msg):
            self.middleware(HttpRequest())
