
from service import check_service_status


def test_status_200():
    assert check_service_status(200) is True


def test_status_201():
    assert check_service_status(201) is False


def test_status_400():
    assert check_service_status(400) is False


def test_status_404():
    assert check_service_status(404) is False


def test_status_500():
    assert check_service_status(500) is False
