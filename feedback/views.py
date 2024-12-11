from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from .models import Feedback, FeedbackTask
from .serializers import FeedbackSerializer
from .tasks import process_feedback

class FeedbackProcessView(APIView):
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data, many=True)
        if serializer.is_valid():
            feedback_records = serializer.save()
            task_ids = []

            for record in feedback_records:
                task = process_feedback.delay(record.id)
                FeedbackTask.objects.create(task_id=task.id)
                task_ids.append(task.id)

            return Response({'task_ids': task_ids}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FeedbackResultsView(APIView):
    def get(self, request, task_id):
        try:
            task_result = AsyncResult(task_id)
            task_entry = FeedbackTask.objects.get(task_id=task_id)

            if task_result.state == 'SUCCESS':
                result = task_result.result
                feedback_id = result.get('feedback_id')
                try:
                    feedback = Feedback.objects.get(id=feedback_id)
                    return Response({
                        'feedback_id': feedback.id,
                        'feedback_text': feedback.feedback_text,
                        'sentiment': feedback.sentiment,
                        'keywords': feedback.keywords,
                        'status': feedback.status
                    }, status=status.HTTP_200_OK)

                except Feedback.DoesNotExist:
                    return Response({'error': 'Feedback not found'}, status=status.HTTP_404_NOT_FOUND)

            elif task_result.state == 'FAILURE':
                task_entry.status = 'FAILURE'
                task_entry.save()
                return Response({'error': str(task_result.info)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'status': task_result.state}, status=status.HTTP_200_OK)
        except FeedbackTask.DoesNotExist:
            return Response({'error': 'Invalid task ID'}, status=status.HTTP_404_NOT_FOUND)
