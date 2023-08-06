import os

FLATPAGES_TEMPLATES = [
    {
        "BACKEND": "hibeetemplate.backends.hhibeeiHibeeplates",
        "DIRS": [os.path.join(os.path.dirname(__file__), "templates")],
        "OPTIONS": {
            "context_processors": ("hibeecontrib.auth.context_processors.auth",),
        },
    }
]
