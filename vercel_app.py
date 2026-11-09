"""Vercel entry point: Vercel looks for a WSGI callable named `app` (see pyproject.toml, [tool.vercel])."""
from dash_app import server as app  # noqa: F401  (the Flask object of the Dash app)
