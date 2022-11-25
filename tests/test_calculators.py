from tests import BaseTestCase

class TestCalculators(BaseTestCase):
    
    def setUp(self):
        super().setUp()
        self.app.post('/user/', json=self.user1)
        result = self.app.post('/user/login', json=self.user1login)
        self.token = result.json['token']
        self.headers = {"Authorization": "Bearer " + self.token}

    def test_calculator(self):
        result = self.app.post('/calculator/', json=self.calculator1, headers=self.headers)
        self.assertEqual(result.status_code, 200)

    def test_calculator400(self):
        result = self.app.post('/calculator/', json={}, headers=self.headers)
        self.assertEqual(result.status_code, 400)
    
    def test_calculator400(self):
        result = self.app.post('/calculator/', json=self.user1login, headers=self.headers)
        self.assertEqual(result.status_code, 400)

    def test_get_calculator(self):
        self.app.post('/calculator/', json=self.calculator1, headers=self.headers)
        result = self.app.get('/calculator/1')
        self.assertEqual(result.status_code, 200)

    def test_get_calculator404(self):
        result = self.app.get('/calculator/2')
        self.assertEqual(result.status_code, 404)

    def test_patch_calculator(self):
        self.app.post('/calculator/', json=self.calculator1, headers=self.headers)
        result = self.app.patch('/calculator/1', json=self.calculator1, headers=self.headers)
        self.assertEqual(result.status_code, 200)
    
    def test_patch_calculatoremptyjson400(self):
        self.app.post('/calculator/', json=self.calculator1, headers=self.headers)
        result = self.app.patch('/calculator/1', json={}, headers=self.headers)
        self.assertEqual(result.status_code, 400)
    
    def test_patch_calculatornotvalidjson400(self):
        self.app.post('/calculator/', json=self.calculator1, headers=self.headers)
        result = self.app.patch('/calculator/1', json={"wrong":"wrong"}, headers=self.headers)
        self.assertEqual(result.status_code, 400)

    def test_patch_calculatornotfound(self):
        self.app.post('/calculator/', json=self.calculator1, headers=self.headers)
        result = self.app.patch('/calculator/2', json=self.calculator1, headers=self.headers)
        self.assertEqual(result.status_code, 404)

    def test_get_calculators(self):
        self.app.post('/calculator/', json=self.calculator1, headers=self.headers)
        result = self.app.get('/calculators/')
        self.assertEqual(result.status_code, 200)

    def test_delete_calculator(self):
        self.app.post('/calculator/', json=self.calculator1, headers=self.headers)
        result = self.app.delete('/calculator/1', headers=self.headers)
        self.assertEqual(result.status_code, 200)