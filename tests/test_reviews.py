from tests import BaseTestCase

class TestReviews(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.app.post('/user/', json=self.user1)
        result = self.app.post('/user/login', json=self.user1login)
        self.token = result.json['token']
        self.headers = {"Authorization": "Bearer " + self.token}
        result = self.app.post('/calculator/', json=self.calculator1, headers=self.headers)

    def test_review_add(self):
        result = self.app.post('/calculators/1/reviews', headers=self.headers, json=self.review1)
        self.assertEqual(result.status_code, 200)
    
    def test_review404(self):
        result = self.app.get('/calculators/2/reviews')
        self.assertEqual(result.status_code, 404)

    def test_get_reviews(self):
        self.app.post('/calculators/1/reviews', headers=self.headers, json=self.review1)
        result = self.app.get('/calculators/1/reviews')
        self.assertEqual(result.status_code, 200)

    def test_patch_review(self):
        self.app.post('/calculators/1/reviews', headers=self.headers, json=self.review1)
        result = self.app.patch('/review/1', headers=self.headers, json=self.review1)
        self.assertEqual(result.status_code, 200)

    def test_patch_review400(self):
        self.app.post('/calculators/1/reviews', headers=self.headers, json=self.review1)
        result = self.app.patch('/review/1', headers=self.headers, json={})
        self.assertEqual(result.status_code, 400)

    def test_delete_review(self):
        self.app.post('/calculators/1/reviews', headers=self.headers, json=self.review1)
        result = self.app.delete('/review/1', headers=self.headers)
        self.assertEqual(result.status_code, 204)