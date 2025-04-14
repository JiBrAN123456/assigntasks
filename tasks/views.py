from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Task
from .serializers import TaskSerialzier


class TaskListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.all()


        status = request.query_params.get("status")
        assigned_user = request.query_params.get("assigned_user")
        deadline_before = request.query_params.get("deadline_before")
        deadline_after = request.query_params.get("deadlne_after")
        is_pending = request.query_params.get("is_pending")

        if status:
            tasks = tasks.filter(status=status)

        if assigned_user:
            tasks = tasks.filter(assigned_users__id=assigned_user)

        if deadline_before:
            tasks = tasks.filter(deadline__lte=deadline_before)

        if deadline_after:
            tasks = tasks.filter(deadline__gte=deadline_after)

        if is_pending == 'true':
            now = timezone.now()
            tasks = tasks.filter(status='pending').filter(deadline__isnull=True) | \
                    tasks.filter(status='pending', deadline__gt=now)

        serializer = TaskSerialzier(tasks.distinct(), many=True)
        return Response(serializer.data)
