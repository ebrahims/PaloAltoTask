
ENDPOINT_IP='http://localhost'
ENDPOINT_PORT = '8000'

REST_API_URL = ENDPOINT_IP+':'+ENDPOINT_PORT+'/players?page={0}'
MAX_PAGE = 3000

USERNAME = 'admin'
PASSWORD = 'admin'
LOAD_TEST_REQUESTS = 20
LOAD_TEST_WORKERS = 5