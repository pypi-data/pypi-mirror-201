__all__ = ["webapp_app"]

from .app import webapp_app
from .header import header_app
from .ssl import ssl_app
from .static import static_app

webapp_app.add_typer(static_app, name="static")
webapp_app.add_typer(header_app, name="header")
webapp_app.add_typer(ssl_app, name="ssl")
