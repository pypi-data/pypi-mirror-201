__all__ = (
    "console_app",
    "file_app",
    "students_app",
    "system_app",
    "scheduled_app",
    "webapp_app",
)

from .console import console_app
from .file import file_app
from .students import students_app
from .system import system_app
from .task import scheduled_app
from .webapp import webapp_app
