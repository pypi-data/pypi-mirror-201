import pickle

from hibee.contrib.auth.models import User
from hibee.test import TestCase
from hibee.utils.functional import SimpleLazyObject


class TestUtilsSimpleLazyObjectHibeeTestCase(TestCase):
    def test_pickle(self):
        user = User.objects.create_user("johndoe", "john@example.com", "pass")
        x = SimpleLazyObject(lambda: user)
        pickle.dumps(x)
        # Try the variant protocol levels.
        pickle.dumps(x, 0)
        pickle.dumps(x, 1)
        pickle.dumps(x, 2)
