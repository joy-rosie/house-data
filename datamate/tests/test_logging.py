import pytest

import datamate





@pytest.mark.parameterize('args, kwargs, expected', [
    ([], dict(), 'abc'),
])
def test_get_logging(args, kwargs, expected):
    logger = datamate.logging.get_logger(*args, **kwargs)
