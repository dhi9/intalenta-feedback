from celery import shared_task, group, chord
from .models import Feedback, FeedbackTask
import random

@shared_task(bind=True, max_retries=3)
def process_feedback(self, feedback_id):
    try:
        feedback = Feedback.objects.get(id=feedback_id)
        feedback.status = 'PROCESSING'
        feedback.save()

        feedback_text = feedback.feedback_text
        tasks = group(
            analizeSentiment.s(feedback_text),
            keywordsExtraction.s(feedback_text)
        )
        callback = save_results.s(feedback_id)
        chord(tasks)(callback)
        
        return {
            'feedback_id': feedback_id,
            'feedback_text': feedback_text,
            'status': 'Task is processing'
        }

    except Feedback.DoesNotExist:
        raise self.retry(exc="Feedback with given ID does not exist.", countdown=5)

    except Exception as e:
        raise self.retry(exc=e, countdown=5)


@shared_task
def analizeSentiment(feedback_text):
    """
    Analyze the sentiment of the feedback text.
    """
    sentiment = random.choice(['positive', 'neutral', 'negative'])
    return sentiment


@shared_task
def keywordsExtraction(feedback_text):
    """
    Extract keywords from the feedback text.
    """
    keywords = ['keyword1', 'keyword2']
    return keywords

@shared_task
def save_results(results, feedback_id):
    """
    Save the sentiment and keywords results to the database.
    """
    try:
        sentiment = results[0]
        keywords = results[1]

        feedback = Feedback.objects.get(id=feedback_id)
        feedback.sentiment = sentiment
        feedback.keywords = keywords
        feedback.status = 'COMPLETED'
        feedback.save()

        return {
            'feedback_id': feedback_id,
            'sentiment': sentiment,
            'keywords': keywords
        }
    except Exception as e:
        print(f"Error in save_results: {e}")
        raise e