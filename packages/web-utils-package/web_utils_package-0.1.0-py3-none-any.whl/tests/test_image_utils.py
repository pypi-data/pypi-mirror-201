"""
This module contains unit tests for the image_utils module
"""
import shutil

import requests

from app.image_utils import get_image


# define a test function that tests the get_image function
# use pytest framework
# test that the function returns True
# Mock requests.get() to return a 200 status code
# Mock shutil.copyfileobj() to return None
# Mock requests.get to return raw data
# Mock requests.get to return raw.decode_content
def test_get_image_mocking_requests(monkeypatch):
    class MockRaw:
        def __init__(self):
            self.decode_content = False

    class MockResponse:
        def __init__(self, raw, status_code):
            self.raw = raw
            self.status_code = status_code

    def mock_get(*args, **kwargs):
        # pylint: disable=unused-argument
        return MockResponse(MockRaw(), 200)

    def mock_copyfileobj(*args, **kwargs):
        # pylint: disable=unused-argument
        return None

    monkeypatch.setattr(requests, "get", mock_get)
    monkeypatch.setattr(shutil, "copyfileobj", mock_copyfileobj)

    # mock open() context manager to return file object but not write to disk
    class MockFile:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *args, **kwargs):
            pass

    monkeypatch.setattr("builtins.open", MockFile)

    assert (
        get_image(
            "https://th.bing.com/th/id/R.b8ec1594a119c65471d8de42c292167",
            "test3.jpg",
        )
        is True
    )


def test_get_image_mocking_requests_error(monkeypatch):
    class MockResponse:
        def __init__(self, status_code):
            self.status_code = status_code

    def mock_get(*args, **kwargs):
        # pylint: disable=unused-argument
        return MockResponse(404)

    monkeypatch.setattr(requests, "get", mock_get)

    assert (
        get_image(
            "https://th.bing.com/th/id/=ajQniVSg%2bLiKoa5Y5s4SDMU%3d&r",
            "test4.jpg",
        )
        is False
    )


# define a test function that tests the get_image function
# use pytest framework


# def test_get_image():
#     # define a test function that tests the get_image function
#     # use pytest framework
#     # test that the function returns None
#     assert (
#         get_image(
#             "https://th.bing.com/th/id/R.b8ec1594a119c65471d8de42c2921672?rik=D%2bE0wUunfURXFw&riu=http%3a%2f%2f2.bp.blogspot.com%2f_LnPUykCeIyY%2fTKs_vjcybYI%2fAAAAAAAAAjQ%2faWnX_koKKyU%2fs1600%2fDSC_0025.jpg&ehk=ajQniVSg%2bLiKoa5Y5sjRRwe1Ef%2b34TFG2G1bnC4SDMU%3d&risl=&pid=ImgRaw&r=0",
#             "test2.jpg",
#         )
#         is True
#     )


# define a test funcion that tests the get_image function
# use pytest framework
# test that the function returns False
# I mean, the function should return False if the image is not downloaded
# def test_get_image_not_downloaded():
#     assert (
#         get_image(
#             "https://th.bing.com/th/id/R.fcd349af80rsf4e5a32bc3696019cf5f?rik=8bH1xMwmkghXvg&pid=ImgRaw&r=0",
#             "test.jpg",
#         )
#         == False
#     )
