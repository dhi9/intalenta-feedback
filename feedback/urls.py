from django.urls import path
from .views import FeedbackProcessView, FeedbackResultsView

urlpatterns = [
    path('process/', FeedbackProcessView.as_view(), name='feedback-process'),
    path('results/<str:task_id>/', FeedbackResultsView.as_view(), name='feedback-results'),
]
