import unittest
import collections
if not hasattr(collections, 'Callable'):
    import collections.abc
    collections.Callable = collections.abc.Callable

from service import app, routes


class TestAccountService(unittest.TestCase):
    def setUp(self):
        # Reset the database before each test
        routes.accounts = {}
        routes.next_id = 1
        self.app = app.test_client()

    def test_security_headers(self):
        """Mengecek apakah security headers ada"""
        response = self.app.get('/accounts')
        self.assertEqual(response.headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertEqual(response.headers.get('X-Frame-Options'), 'DENY')

    def test_cors_security(self):
        """Mengecek apakah CORS diizinkan"""
        response = self.app.get('/accounts')
        self.assertEqual(response.headers.get('Access-Control-Allow-Origin'), '*')

    def test_create_account(self):
        """Create a new account"""
        response = self.app.post('/accounts', json={
            "name": "John Doe",
            "email": "john@example.com",
            "address": "Jakarta"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["name"], "John Doe")

    def test_list_accounts(self):
        """List all accounts"""
        self.app.post('/accounts', json={"name": "A"})
        self.app.post('/accounts', json={"name": "B"})
        response = self.app.get('/accounts')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 2)

    def test_get_account(self):
        """Get a single account"""
        resp = self.app.post('/accounts', json={"name": "A"})
        acc_id = resp.get_json()["id"]
        response = self.app.get(f'/accounts/{acc_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "A")

    def test_get_account_not_found(self):
        """Get a single account not found"""
        response = self.app.get('/accounts/999')
        self.assertEqual(response.status_code, 404)

    def test_update_account(self):
        """Update an account"""
        resp = self.app.post('/accounts', json={"name": "A"})
        acc_id = resp.get_json()["id"]
        response = self.app.put(f'/accounts/{acc_id}', json={"name": "B"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "B")

    def test_update_account_not_found(self):
        """Update an account not found"""
        response = self.app.put('/accounts/999', json={"name": "B"})
        self.assertEqual(response.status_code, 404)

    def test_delete_account(self):
        """Delete an account"""
        resp = self.app.post('/accounts', json={"name": "A"})
        acc_id = resp.get_json()["id"]
        response = self.app.delete(f'/accounts/{acc_id}')
        self.assertEqual(response.status_code, 200)
        # Verify it's deleted
        response2 = self.app.get(f'/accounts/{acc_id}')
        self.assertEqual(response2.status_code, 404)

    def test_delete_account_not_found(self):
        """Delete an account not found"""
        response = self.app.delete('/accounts/999')
        self.assertEqual(response.status_code, 404)
