import unittest
from app import app

class TestAppMethods(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_App_badUrl(self):
        response = self.app.post("/get_reviews", data=dict(url="www.test.com"))
        assert b"Must be a lendingtree review page" in response.data

    def test_App_badUrlPath(self):
        response = self.app.post("/get_reviews", data=dict(url="www.lendingtree.com/test"))
        assert b"Must be a lendingtree review page" in response.data

    # originally I had code checking if url was none after getting the form data,
    # but it looks like flask will already throw a bad request for that
    def test_App_noUrl(self):
        response = self.app.post("/get_reviews")
        assert b"Bad Request" in response.data

    # I spent a long time looking at the Werkzeug docs to figure out how to check for a response
    # code specifically when json is returned but had trouble finding anything, 
    # so instead this test just ensures that the respone is not a bad request
    def test_app_integration(self):
        response = self.app.post("/get_reviews", data=dict(url="https://www.lendingtree.com/reviews/personal/lendingclub/33829657?sort=cmV2aWV3c3VibWl0dGVkX2FzYw==&pid=1"))
        assert b"Bad Request" not in response.data

if __name__ == '__main__':
    unittest.main()