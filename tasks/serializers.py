from rest_framework import serializers
from .models import Task, User
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email','mobile']


class TaskSerialzier(serializers.ModelSerializer):
    assigned_users = UserSerializer(many=True, read_only = True)
    assigned_user_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many = True,
        write_only = True,
        source = "assigned_users"
    )       
    
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    completed_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, allow_null=True)
    deadline = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_pending = serializers.SerializerMethodField() 

    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'description',
            'task_type',
            'created_at',
            'completed_at',
            'deadline',
            'status',
            'status_display',
            'is_pending',
            'assigned_users',
            'assigned_user_ids',
        ]

    def get_is_pending(self,obj):
        return obj.status == 'pending'  and (obj.deadline is None or obj.deadline > timezone.now())   
    

    def validate(self, attrs):
        status = attrs.get("status")
        completed_at = attrs.get('completed_at')
        if status == "compledted" and not completed_at:
            raise serializers.ValidationError("completed_at must be set if status is 'completed'.")
        return attrs 
    