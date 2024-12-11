from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from feedback.models import Feedback
from unittest.mock import patch

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

    @patch('feedback.tasks.analizeSentiment.s')
    @patch('feedback.tasks.keywordsExtraction.s')
    def test_process_feedback_success(self, mock_keywords, mock_sentiment):
        mock_sentiment.return_value.get.return_value = 'positive'
        mock_keywords.return_value.get.return_value = ['good', 'quality']

        response = self.client.post(self.url, [{
            'feedback_id': self.feedback.id,
            'customer_id': self.feedback.customer_id,
            'feedback_text': self.feedback.feedback_text,
            'timestamp': self.feedback.timestamp
        }], format='json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('task_ids', response.data)

    @patch('feedback.tasks.analizeSentiment.s')
    @patch('feedback.tasks.keywordsExtraction.s')
    def test_process_feedback_invalid(self, mock_keywords, mock_sentiment):
        mock_sentiment.return_value.get.return_value = 'negative'
        mock_keywords.return_value.get.return_value = ['bad', 'poor']

        # Simulating an invalid without required fields
        response = self.client.post(self.url, [{
            'feedback_text': 'Invalid feedback',
            'timestamp': '2024-12-11T12:00:00Z'
        }], format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
