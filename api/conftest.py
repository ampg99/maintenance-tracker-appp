# conftest.py
import pytest

from run import create_app


@pytest.fixture
def app():
    app = create_app(filename='config')
    app.debug = True
    return app