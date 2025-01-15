from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'rate', 'description',
                  'days_required', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'user']
