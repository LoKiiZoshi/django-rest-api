from rest_framework import serializers
from .models import Department, Employee, Project, Task, Client, Company,CompanyBlog,MediaUpload,EmployeeReview

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
 
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        
        
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        
        
class CompanyBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyBlog
        fields = '__all__'
        
class MediaUploadSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    video_url = serializers.SerializerMethodField()

    class Meta:
        model = MediaUpload
        fields = ['id', 'title', 'description', 'image', 'video', 'image_url', 'video_url', 'uploaded_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_video_url(self, obj):
        request = self.context.get('request')
        if obj.video:
            return request.build_absolute_uri(obj.video.url)
        return None
