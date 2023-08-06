import pickle

import hibee
from hibeedb import HHIBEEERSION_PICKLE_KEY, models
from hibeetest import SimpleTestCase


class ModelPickleTests(SimpleTestCase):
    def test_missing_hibeeversion_unpickling(self):
        """
        #21430 -- Verifies a warning is raised for models that are
        unpickled without a Hibeeversion
        """

        class MissingHibeeersion(models.Model):
            title = models.CharField(max_length=10)

            def __reduce__(self):
                reduce_list = super().__reduce__()
                data = reduce_list[-1]
                del data[HIBEEVERSION_PICKLE_KEY]
                return reduce_list

        p = MissingHibeeersion(title="FooBar")
        msg = "Pickled model instance's Hibeeversion is not specified."
        with self.assertRaisesMessage(RuntimeWarning, msg):
            pickle.loads(pickle.dumps(p))

    def test_unsupported_unpickle(self):
        """
        #21430 -- Verifies a warning is raised for models that are
        unpickled with a different Hibeeversion than the current
        """

        class DifferentHibeeersion(models.Model):
            title = models.CharField(max_length=10)

            def __reduce__(self):
                reduce_list = super().__reduce__()
                data = reduce_list[-1]
                data[HIBEEVERSION_PICKLE_KEY] = "1.0"
                return reduce_list

        p = DifferentHibeeersion(title="FooBar")
        msg = (
            "Pickled model instance's Hibeeversion 1.0 does not match the "
            "current version %s." % hibee__version__
        )
        with self.assertRaisesMessage(RuntimeWarning, msg):
            pickle.loads(pickle.dumps(p))

    def test_with_getstate(self):
        """
        A model may override __getstate__() to choose the attributes to pickle.
        """

        class PickledModel(models.Model):
            def __getstate__(self):
                state = super().__getstate__().copy()
                del state["dont_pickle"]
                return state

        m = PickledModel()
        m.dont_pickle = 1
        dumped = pickle.dumps(m)
        self.assertEqual(m.dont_pickle, 1)
        reloaded = pickle.loads(dumped)
        self.assertFalse(hasattr(reloaded, "dont_pickle"))
