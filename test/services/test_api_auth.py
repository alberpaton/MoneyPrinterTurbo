import unittest

from app.utils.api_auth import is_authorized


class TestApiAuth(unittest.TestCase):
    def test_no_token_means_open(self):
        self.assertTrue(is_authorized("/api/v1/videos", "POST", {}, ""))

    def test_api_requires_bearer(self):
        self.assertFalse(is_authorized("/api/v1/videos", "POST", {}, "s3cret"))
        self.assertFalse(
            is_authorized("/api/v1/videos", "POST", {"authorization": "Bearer nope"}, "s3cret")
        )
        self.assertTrue(
            is_authorized("/api/v1/videos", "POST", {"authorization": "Bearer s3cret"}, "s3cret")
        )

    def test_x_api_key_also_works(self):
        self.assertTrue(is_authorized("/api/v1/tasks", "GET", {"x-api-key": "s3cret"}, "s3cret"))

    def test_preflight_and_non_api_paths_stay_open(self):
        self.assertTrue(is_authorized("/api/v1/videos", "OPTIONS", {}, "s3cret"))
        self.assertTrue(is_authorized("/tasks/abc/final-1.mp4", "GET", {}, "s3cret"))
        self.assertTrue(is_authorized("/", "GET", {}, "s3cret"))


if __name__ == "__main__":
    unittest.main()
