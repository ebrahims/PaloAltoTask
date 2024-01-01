
import pytest
import requests

from constants import USERNAME, PASSWORD, ENDPOINT_PORT, REST_API_URL
from utils import lunch_server, free_port


@pytest.fixture
def api_session(request):
    try:
        user_name = request.param.get('username', USERNAME)
    except AttributeError:
        user_name = USERNAME
    try:
        password = request.param.get('password', PASSWORD)
    except AttributeError:
        password = PASSWORD
    lunch_server()
    url = REST_API_URL.format('1')
    session = requests.sessions.Session()
    session.auth = (user_name, password)
    session.get(url)
    return session

def pytest_sessionfinish(session, exitstatus):
    free_port(ENDPOINT_PORT)