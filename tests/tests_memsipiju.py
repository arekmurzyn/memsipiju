import unittest
from memsipiju import app
from io import StringIO
import sys

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.captured_output = StringIO()
        sys.stdout = self.captured_output
        sys.stderr = self.captured_output

    def tearDown(self):
        self.app = None
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def test_valid_request(self):
        response = self.app.post('/job', json={'duration': 1.0, 'memory_mb': 100})
        data = response.get_json()
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert data['status'] == 'completed', f"Expected 'completed', got {data['status']}"

    def test_invalid_json(self):
        response = self.app.post('/job', data='{"not": "json"}')
        data = response.get_json()
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        assert data['error'] == 'Request must be JSON', f"Expected 'Request must be JSON', got {data['error']}"

    def test_missing_duration(self):
        response = self.app.post('/job', json={'memory_mb': 100})
        data = response.get_json()
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        assert data['error'] == 'Duration parameter is required', f"Expected 'Duration parameter is required', got {data['error']}"

    def test_missing_memory(self):
        response = self.app.post('/job', json={'duration': 1})
        data = response.get_json()
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        assert data['error'] == 'Memory amount parameter is required', f"Expected 'Memory amount parameter is required', got {data['error']}"

    def test_invalid_duration(self):
        response = self.app.post('/job', json={'duration': 'not_a_number', 'memory_mb': 100})
        data = response.get_json()
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        assert data['error'] == 'Duration must be a positive number', f"Expected 'Duration must be a positive number', got {data['error']}"

    def test_invalid_memory(self):
        response = self.app.post('/job', json={'duration': 1, 'memory_mb': 'not a number'})
        data = response.get_json()
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        assert data['error'] == 'Memory amount must be a positive number', f"Expected 'Memory amount must be a positive number', got {data['error']}"

    def test_negative_memory(self):
        response = self.app.post('/job', json={'duration': 1.0, 'memory_mb': -100})
        data = response.get_json()
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        assert data['error'] == 'Memory amount must be a positive number', f"Expected 'Memory amount must be a positive number', got {data['error']}"

    def test_negative_duration(self):
        response = self.app.post('/job', json={'duration': -1.0, 'memory_mb': 100})
        data = response.get_json()
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        assert data['error'] == 'Duration must be a positive number', f"Expected 'Duration must be a positive number', got {data['error']}"

if __name__ == '__main__':
    import nose
    nose.main()