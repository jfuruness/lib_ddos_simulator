import pytest

from ..api import create_app


@pytest.fixture(scope="package")
def app():
    """Create and configure a new app instance for each test."""
    # create the app with common test config
    app = create_app()

    yield app


@pytest.fixture(scope="package")
def client(app):
    """A test client for the app."""
    return app.test_client()
