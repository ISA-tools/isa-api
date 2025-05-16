import unittest
from unittest.mock import patch
from isatools.net.storage_adapter import IsaGitHubStorageAdapter


class TestIsaGitHubStorageAdapter(unittest.TestCase):

    @patch('isatools.net.storage_adapter.requests.get')
    def test_is_not_authenticated(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = []
        adapter = IsaGitHubStorageAdapter()
        self.assertFalse(adapter.is_authenticated)


    @patch('isatools.net.storage_adapter.requests.get')
    @patch('isatools.net.storage_adapter.requests.post')
    def test_authorization_creation(self, mock_get, mock_post):
        # Mock the GET request
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = []
        # Mock the POST request
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"token": None}

        adapter = IsaGitHubStorageAdapter(username="user", password="pass")
        self.assertEqual(adapter.token, None)


    @patch('isatools.net.storage_adapter.requests.get')
    @patch('isatools.net.storage_adapter.requests.delete')
    def test_close(self, mock_get, mock_delete):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = []
        mock_delete.return_value.status_code = 204
        adapter = IsaGitHubStorageAdapter(username="user", password="pass")
        adapter.close()
        mock_delete.assert_called_once()

    # @patch('isatools.net.storage_adapter.requests.get')
    # def test_download_json(self, mock_get):
    #     # Mock the GET request to return a valid JSON response
    #     mock_get.return_value.status_code = 200
    #     mock_get.return_value.json.return_value = {"key": "value"}
    #     adapter = IsaGitHubStorageAdapter()
    #     result = adapter.download(source="test.json", destination="test_dir")
    #     self.assertTrue(result)

    @patch('isatools.net.storage_adapter.requests.get')
    def test_download_invalid_file(self, mock_get):
        mock_get.return_value.status_code = 404
        adapter = IsaGitHubStorageAdapter()
        result = adapter.download(source="invalid.json", destination="test_dir")
        self.assertFalse(result)

    # @patch('isatools.net.storage_adapter.requests.get')
    # def test_retrieve_json(self, mock_get):
    #     mock_get.return_value.status_code = 200
    #     mock_get.return_value.json.return_value = {"key": "value"}
    #     adapter = IsaGitHubStorageAdapter(username="user", password="pass")
    #     result = adapter.retrieve(source="test.json")
    #     self.assertEqual(result, {"key": "value"})
    #
    # @patch('isatools.net.storage_adapter.requests.get')
    # def test_retrieve_invalid_file(self, mock_get):
    #     mock_get.return_value.status_code = 404
    #     adapter = IsaGitHubStorageAdapter(username="user", password="pass")
    #     with self.assertRaises(Exception):
    #         adapter.retrieve(source="invalid.json")

    @patch('isatools.net.storage_adapter.base64.b64decode')
    def test_handle_content_json(self, mock_decode):
        mock_decode.return_value = b'{"key": "value"}'
        adapter = IsaGitHubStorageAdapter()
        payload = {"encoding": "base64", "content": "test", "name": "test.json"}
        result = adapter._handle_content(payload)
        self.assertEqual(result["json"], {"key": "value"})

    @patch('isatools.net.storage_adapter.base64.b64decode')
    def test_handle_content_invalid(self, mock_decode):
        mock_decode.return_value = b'invalid content'
        adapter = IsaGitHubStorageAdapter()
        payload = {"encoding": "base64", "content": "test", "name": "test.txt"}
        result = adapter._handle_content(payload)
        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
