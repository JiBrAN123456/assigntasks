from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Task , User
from .serializers import TaskSerialzier
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.generics import RetrieveAPIView


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




class TaskCreateAPIView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerialzier
    permission_classes = [IsAuthenticated]



class TaskDetailAPIView(RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerialzier
    permission_classes = [IsAuthenticated]



class AssignTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        user_ids = request.data.get("user_ids",[])
        users = User.objects.filter(id__in=user_ids)
        task.assigned_users.set(users)
        return Response({"message":"Users assigned successfully"})