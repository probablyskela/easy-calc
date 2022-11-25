from tests import BaseTestCase

class TestUsers(BaseTestCase):
    def test_user_create(self):
        result = self.app.post('/user/', json=self.user1)
        self.assertEqual(result.status_code, 200)

    def test_user_create400(self):
        result = self.app.post('/user/', json=self.user1login)
        self.assertEqual(result.status_code, 400)

    def test_user_login(self):
        self.app.post('/user/', json=self.user1)
        result = self.app.post('/user/login', json=self.user1login)
        self.assertEqual(result.status_code, 200)
        self.token = result.json['token']

    def test_user_login400(self):
        result = self.app.post('/user/login', json=self.user1)
        self.assertEqual(result.status_code, 400)

    def test_user_patch(self):
        self.app.post('/user/', json=self.user1)
        result = self.app.post('/user/login', json=self.user1login)
        token = result.json['token']
        result = self.app.patch('/user/1', json=self.user1, headers = {"Authorization": "Bearer " + token})
        self.assertEqual(result.status_code, 200)
    def test_user_patch404(self):
        self.app.post('/user/', json=self.user1)
        result = self.app.post('/user/login', json=self.user1login)
        token = result.json['token']
        result = self.app.patch('/user/2', json=self.user1, headers = {"Authorization": "Bearer " + token})
        self.assertEqual(result.status_code, 404)
    def test_user_patch400(self):
        self.app.post('/user/', json=self.user1)
        result = self.app.post('/user/login', json=self.user1login)
        token = result.json['token']
        result = self.app.patch('/user/1', json={}, headers = {"Authorization": "Bearer " + token})
        self.assertEqual(result.status_code, 400)    
    def test_user_patchinvalid400(self):
        self.app.post('/user/', json=self.user1)
        result = self.app.post('/user/login', json=self.user1login)
        token = result.json['token']
        result = self.app.patch('/user/1', json={"wrong":1}, headers = {"Authorization": "Bearer " + token})
        self.assertEqual(result.status_code, 400)
    def test_user_patch403(self):
        self.app.post('/user/', json=self.user1)
        self.app.post('/user/', json=self.user2)
        result = self.app.post('/user/login', json=self.user2login)
        token = result.json['token']
        result = self.app.patch('/user/1', json=self.user1, headers = {"Authorization": "Bearer " + token})
        self.assertEqual(result.status_code, 403)

    def test_delete_user(self):
        self.app.post('/user/', json=self.user1)
        result = self.app.post('/user/login', json=self.user1login)
        token = result.json['token']
        result = self.app.delete('/user/1', headers = {"Authorization": "Bearer " + token})
        self.assertEqual(result.status_code, 204)
    def test_delete_user404(self):
        self.app.post('/user/', json=self.user1)
        result = self.app.post('/user/login', json=self.user1login)
        token = result.json['token']
        result = self.app.delete('/user/2', headers = {"Authorization": "Bearer " + token})
        self.assertEqual(result.status_code, 404)
    def test_delete_user403(self):
        self.app.post('/user/', json=self.user1)
        self.app.post('/user/', json=self.user2)
        result = self.app.post('/user/login', json=self.user2login)
        token = result.json['token']
        result = self.app.delete('/user/1', headers = {"Authorization": "Bearer " + token})
        self.assertEqual(result.status_code, 403)


