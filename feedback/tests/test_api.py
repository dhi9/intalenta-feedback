from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from feedback.models import Feedback

class FeedbackApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a dummy feedback entry
        self.feedback_data = {
            'customer_id': 123,
            'feedback_text': 'Great product!',
            'timestamp': '2024-12-11T12:00:00Z'
        }
        self.feedback = Feedback.objects.create(**self.feedback_data)
        self.url = reverse('feedback-process')

    def test_process_feedback_success(self):
        response = self.client.post(self.url, [{
            'feedback_id': self.feedback.id,
            'customer_id': self.feedback.customer_id,
            'feedback_text': self.feedback.feedback_text,
            'timestamp': self.feedback.timestamp
        }], format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('task_ids', response.data)

    def test_process_feedback_invalid(self):
        response = self.client.post(self.url, {'feedback_id': "invalid"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
