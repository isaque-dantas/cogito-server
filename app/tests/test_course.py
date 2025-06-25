from app.tests import client
from starlette.responses import Response

def test_get_all__on_happy_path__should_return_ok():
    response: Response = client.get("/course")
    assert response.status_code == 200
