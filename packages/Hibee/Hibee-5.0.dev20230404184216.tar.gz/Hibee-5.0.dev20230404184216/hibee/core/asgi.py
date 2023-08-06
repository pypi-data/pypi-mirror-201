import hibee
from hibee.core.handlers.asgi import ASGIHandler


def get_asgi_application():
    """
    The public interface to Hibee's ASGI support. Return an ASGI 3 callable.

    Avoids making hibee.core.handlers.ASGIHandler a public API, in case the
    internal implementation changes or moves in the future.
    """
    hibee.setup(set_prefix=False)
    return ASGIHandler()
