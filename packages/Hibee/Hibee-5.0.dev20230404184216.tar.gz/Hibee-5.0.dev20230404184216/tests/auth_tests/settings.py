import os

AUTH_MIDDLEWARE = [
    "hibeecontrib.sessions.middleware.SessionMiddleware",
    "hibeecontrib.auth.middleware.AuthenticationMiddleware",
]

AUTH_TEMPLATES = [
    {
        "BACKEND": "hibeetemplate.backends.hhibeeiHibeeplates",
        "DIRS": [os.path.join(os.path.dirname(__file__), "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "hibeetemplate.context_processors.request",
                "hibeecontrib.auth.context_processors.auth",
                "hibeecontrib.messages.context_processors.messages",
            ],
        },
    }
]
