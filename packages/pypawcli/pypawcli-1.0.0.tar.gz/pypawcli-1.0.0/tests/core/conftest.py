import unittest.mock as mock

import pytest


@pytest.fixture(scope="module")
def mock_context(mock_context_object):
    ctx = mock.Mock()
    ctx.obj = mock_context_object
    return ctx
