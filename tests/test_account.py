import unittest
import collections
if not hasattr(collections, 'Callable'):
    import collections.abc
    collections.Callable = collections.abc.Callable

# Mengimpor create_app karena di __init__.py Anda menggunakan fungsi tersebut
from service import create_app 

class TestAccountService(unittest.TestCase):
    def setUp(self):
        self.app = create_app() # Memanggil fungsi untuk membuat instance app
        self.client = self.app.test_client()

    def test_security_headers(self):
        """Mengecek apakah security headers ada"""
        response = self.client.get('/')
        # Kita cek headers dari response
        self.assertEqual(response.headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertEqual(response.headers.get('X-Frame-Options'), 'DENY')

    def test_cors_security(self):
        """Mengecek apakah CORS diizinkan"""
        response = self.client.get('/')
        self.assertEqual(response.headers.get('Access-Control-Allow-Origin'), '*')
