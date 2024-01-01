import concurrent.futures
import time
import pytest
import json

from constants import REST_API_URL, MAX_PAGE, LOAD_TEST_REQUESTS, LOAD_TEST_WORKERS
from utils import send_request, dict_validation


@pytest.mark.order(1)
def test_endpoint_availability(api_session):
    url = REST_API_URL.format(1)
    response = api_session.get(url)
    assert response.status_code == 200


def test_stress_test(api_session):
    sum = 0
    for i in range(MAX_PAGE):
        t_before = time.time()
        r1 = api_session.get(REST_API_URL.format(i))
        t_after = time.time()
        duration=t_after - t_before
        sum+=duration
        print(duration)
    print(sum)


def test_consistent_data_per_page(api_session):
    for i in range(1, MAX_PAGE):
        url = REST_API_URL.format(i)
        r1 = api_session.get(url)
        parsed1 = json.loads(r1.content)
        r2 = api_session.get(url)
        parsed2 = json.loads(r2.content)
        assert dict_validation(parsed1, parsed2)


def test_data_ids_validation(api_session):
    ids = []
    for i in range(1, MAX_PAGE):
        r = api_session.get(REST_API_URL.format(i))
        parsed = json.loads(r.content)
        for player in parsed:
            if player['ID'] not in ids:
                ids.append(player['ID'])
            else:
                raise AssertionError(f'ID duplication')
    assert r.status_code == 401


@pytest.mark.parametrize('api_session', [{'username': 'admin','password':'admin'}], indirect=['api_session'])
def test_user_validation(api_session):
    r = api_session.get(REST_API_URL.format(1))
    assert r.status_code == 200


@pytest.mark.parametrize('api_session', [{'username': 'a'}, {'password': 'amin'}, {'username': 'f', 'password': 'dd'}],
                         indirect=['api_session'])
def test_user_validation_negative(api_session):
    r = api_session.get(REST_API_URL.format(1))
    assert r.status_code == 401


def test_load_test(api_session):
    tasks = [send_request for _ in range(LOAD_TEST_REQUESTS)]
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=LOAD_TEST_WORKERS)
    futures = [executor.submit(task) for task in tasks]
    concurrent.futures.wait(futures)
    send_request()
