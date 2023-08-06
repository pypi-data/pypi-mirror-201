__all__ = ["scheduled_app"]

from .alwayson import alwayson_app
from .scheduled import scheduled_app

scheduled_app.add_typer(alwayson_app, name="aon")
