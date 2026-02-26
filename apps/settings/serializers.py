from rest_framework import serializers
from .models import Branch, Location, Department, ReportType, RiskCategory
from core.exceptions import ValidationError


class BranchSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Branch
        fields = ['id', 'name', 'status', 'address', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class LocationSerializer(serializers.ModelSerializer):
    
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = Location
        fields = ['id', 'name', 'branch', 'branch_name', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class DepartmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ReportTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReportType
        fields = ['id', 'name', 'type_code', 'status', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_type_code(self, value):
        if self.instance and self.instance.type_code == value:
            return value
        if ReportType.objects.filter(type_code=value).exists():
            raise ValidationError('Bu kod allaqachon mavjud')
        return value


class RiskCategorySerializer(serializers.ModelSerializer):
    
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    
    class Meta:
        model = RiskCategory
        fields = ['id', 'name', 'severity', 'severity_display', 'status', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']