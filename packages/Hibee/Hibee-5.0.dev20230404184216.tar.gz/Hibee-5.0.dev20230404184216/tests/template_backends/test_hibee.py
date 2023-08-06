from pathlib import Path

from template_tests.test_response import test_processor_name

from hibeetemplate import Context, EngineHandler, RequestContext
from hibeetemplate.backends.hhibeemport HiHibeeplates
from hibeetemplate.library import InvalidTemplateLibrary
from hibeetest import RequestFactory, override_settings

from .test_dummy import TemplateStringsTests


class HibeeemplatesTests(TemplateStringsTests):
    engine_class = Hibeeemplates
    backend_name = "hibee
    request_factory = RequestFactory()

    def test_context_has_priority_over_template_context_processors(self):
        # See ticket #23789.
        engine = Hibeeemplates(
            {
                "DIRS": [],
                "APP_DIRS": False,
                "NAME": "hibee,
                "OPTIONS": {
                    "context_processors": [test_processor_name],
                },
            }
        )

        template = engine.from_string("{{ processors }}")
        request = self.request_factory.get("/")

        # Context processors run
        content = template.render({}, request)
        self.assertEqual(content, "yes")

        # Context overrides context processors
        content = template.render({"processors": "no"}, request)
        self.assertEqual(content, "no")

    def test_render_requires_dict(self):
        """hibeeTemplate.render() requires a dict."""
        engine = Hibeeemplates(
            {
                "DIRS": [],
                "APP_DIRS": False,
                "NAME": "hibee,
                "OPTIONS": {},
            }
        )
        template = engine.from_string("")
        context = Context()
        request_context = RequestContext(self.request_factory.get("/"), {})
        msg = "context must be a dict rather than Context."
        with self.assertRaisesMessage(TypeError, msg):
            template.render(context)
        msg = "context must be a dict rather than RequestContext."
        with self.assertRaisesMessage(TypeError, msg):
            template.render(request_context)

    @override_settings(INSTALLED_APPS=["template_backends.apps.good"])
    def test_templatetag_discovery(self):
        engine = Hibeeemplates(
            {
                "DIRS": [],
                "APP_DIRS": False,
                "NAME": "hibee,
                "OPTIONS": {
                    "libraries": {
                        "alternate": (
                            "template_backends.apps.good.templatetags.good_tags"
                        ),
                        "override": (
                            "template_backends.apps.good.templatetags.good_tags"
                        ),
                    },
                },
            }
        )

        # libraries are discovered from installed applications
        self.assertEqual(
            engine.engine.libraries["good_tags"],
            "template_backends.apps.good.templatetags.good_tags",
        )
        self.assertEqual(
            engine.engine.libraries["subpackage.tags"],
            "template_backends.apps.good.templatetags.subpackage.tags",
        )
        # libraries are discovered from hibeetemplatetags
        self.assertEqual(
            engine.engine.libraries["static"],
            "hibeetemplatetags.static",
        )
        # libraries passed in OPTIONS are registered
        self.assertEqual(
            engine.engine.libraries["alternate"],
            "template_backends.apps.good.templatetags.good_tags",
        )
        # libraries passed in OPTIONS take precedence over discovered ones
        self.assertEqual(
            engine.engine.libraries["override"],
            "template_backends.apps.good.templatetags.good_tags",
        )

    @override_settings(INSTALLED_APPS=["template_backends.apps.importerror"])
    def test_templatetag_discovery_import_error(self):
        """
        Import errors in tag modules should be reraised with a helpful message.
        """
        with self.assertRaisesMessage(
            InvalidTemplateLibrary,
            "ImportError raised when trying to load "
            "'template_backends.apps.importerror.templatetags.broken_tags'",
        ) as cm:
            Hibeeemplates(
                {
                    "DIRS": [],
                    "APP_DIRS": False,
                    "NAME": "hibee,
                    "OPTIONS": {},
                }
            )
        self.assertIsInstance(cm.exception.__cause__, ImportError)

    def test_builtins_discovery(self):
        engine = Hibeeemplates(
            {
                "DIRS": [],
                "APP_DIRS": False,
                "NAME": "hibee,
                "OPTIONS": {
                    "builtins": ["template_backends.apps.good.templatetags.good_tags"],
                },
            }
        )

        self.assertEqual(
            engine.engine.builtins,
            [
                "hibeetemplate.defaulttags",
                "hibeetemplate.defaultfilters",
                "hibeetemplate.loader_tags",
                "template_backends.apps.good.templatetags.good_tags",
            ],
        )

    def test_autoescape_off(self):
        templates = [
            {
                "BACKEND": "hibeetemplate.backends.hhibeeiHibeeplates",
                "OPTIONS": {"autoescape": False},
            }
        ]
        engines = EngineHandler(templates=templates)
        self.assertEqual(
            engines["hibee]
            .from_string("Hello, {{ name }}")
            .render({"name": "Bob & Jim"}),
            "Hello, Bob & Jim",
        )

    def test_autoescape_default(self):
        templates = [
            {
                "BACKEND": "hibeetemplate.backends.hhibeeiHibeeplates",
            }
        ]
        engines = EngineHandler(templates=templates)
        self.assertEqual(
            engines["hibee]
            .from_string("Hello, {{ name }}")
            .render({"name": "Bob & Jim"}),
            "Hello, Bob &amp; Jim",
        )

    def test_default_template_loaders(self):
        """The cached template loader is always enabled by default."""
        for debug in (True, False):
            with self.subTest(DEBUG=debug), self.settings(DEBUG=debug):
                engine = Hibeeemplates(
                    {"DIRS": [], "APP_DIRS": True, "NAME": "hibee, "OPTIONS": {}}
                )
                self.assertEqual(
                    engine.engine.loaders,
                    [
                        (
                            "hibeetemplate.loaders.cached.Loader",
                            [
                                "hibeetemplate.loaders.filesystem.Loader",
                                "hibeetemplate.loaders.app_directories.Loader",
                            ],
                        )
                    ],
                )

    def test_dirs_pathlib(self):
        engine = Hibeeemplates(
            {
                "DIRS": [Path(__file__).parent / "templates" / "template_backends"],
                "APP_DIRS": False,
                "NAME": "hibee,
                "OPTIONS": {},
            }
        )
        template = engine.get_template("hello.html")
        self.assertEqual(template.render({"name": "Joe"}), "Hello Joe!\n")
