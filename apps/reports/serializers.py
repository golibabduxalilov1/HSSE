from rest_framework import serializers
from django.utils import timezone
from .models import Report, ReportAttachment, ReportComment, ReportHistory
from apps.accounts.serializers import UserSerializer
from apps.settings.serializers import (
    BranchSerializer, LocationSerializer, ReportTypeSerializer, RiskCategorySerializer
)


class ReportAttachmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReportAttachment
        fields = ['id', 'file', 'file_type', 'file_name', 'file_size', 'created_at']
        read_only_fields = ['id', 'created_at', 'file_size']
    
    def create(self, validated_data):
        file = validated_data.get('file')
        validated_data['file_name'] = file.name
        validated_data['file_size'] = file.size
        return super().create(validated_data)


class ReportCommentSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ReportComment
        fields = ['id', 'report', 'user', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class ReportHistorySerializer(serializers.ModelSerializer):
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ReportHistory
        fields = ['id', 'report', 'user', 'action', 'old_value', 'new_value', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class ReportListSerializer(serializers.ModelSerializer):
    
    report_type_name = serializers.CharField(source='report_type.name', read_only=True)
    reporter_name = serializers.CharField(source='reporter.full_name', read_only=True)
    assignee_name = serializers.CharField(source='assignee.full_name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    attachments_count = serializers.IntegerField(source='attachments.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    
    class Meta:
        model = Report
        fields = [
            'id', 'code', 'title', 'description',
            'report_type', 'report_type_name',
            'reporter', 'reporter_name',
            'assignee', 'assignee_name',
            'branch', 'branch_name',
            'location', 'location_name',
            'status', 'status_display',
            'priority', 'priority_display',
            'deadline', 'attachments_count', 'comments_count',
            'created_at', 'updated_at'
        ]


class ReportDetailSerializer(serializers.ModelSerializer):
    
    report_type = ReportTypeSerializer(read_only=True)
    risk_category = RiskCategorySerializer(read_only=True)
    branch = BranchSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    reporter = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)
    attachments = ReportAttachmentSerializer(many=True, read_only=True)
    comments = ReportCommentSerializer(many=True, read_only=True)
    history = ReportHistorySerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    class Meta:
        model = Report
        fields = [
            'id', 'code', 'title', 'description',
            'report_type', 'risk_category',
            'branch', 'location',
            'reporter', 'assignee',
            'status', 'status_display',
            'priority', 'priority_display',
            'start_date', 'deadline', 'completed_date',
            'is_anonymous',
            'attachments', 'comments', 'history',
            'created_at', 'updated_at'
        ]


class ReportCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Report
        fields = [
            'title', 'description',
            'report_type', 'risk_category',
            'branch', 'location',
            'is_anonymous'
        ]
    
    def create(self, validated_data):
        validated_data['reporter'] = self.context['request'].user
        validated_data['status'] = 'new'
        return super().create(validated_data)


class ReportUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Report
        fields = [
            'title', 'description',
            'risk_category',
            'assignee',
            'status',
            'priority',
            'start_date',
            'deadline',
            'completed_date'
        ]
    
    def update(self, instance, validated_data):
        old_status = instance.status
        new_status = validated_data.get('status', old_status)
        
        if old_status != new_status:
            if new_status == 'completed':
                validated_data['completed_date'] = timezone.now().date()
        
        return super().update(instance, validated_data)


class ReportStatisticsSerializer(serializers.Serializer):
    
    total_reports = serializers.IntegerField()
    new_reports = serializers.IntegerField()
    in_progress_reports = serializers.IntegerField()
    completed_reports = serializers.IntegerField()
    cancelled_reports = serializers.IntegerField()
    
    nearmiss_count = serializers.IntegerField()
    observation_count = serializers.IntegerField()
    accident_count = serializers.IntegerField()
    incident_count = serializers.IntegerField()
    
    by_status = serializers.DictField()
    by_type = serializers.DictField()
    by_priority = serializers.DictField()
    by_branch = serializers.DictField()
    monthly_stats = serializers.DictField()