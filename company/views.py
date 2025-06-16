from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Department, Employee, Project, Task, Client,Company,MediaUpload,CompanyBlog
from .serializers import DepartmentSerializer, EmployeeSerializer, ProjectSerializer, TaskSerializer, ClientSerializer,CompanySerializer,MediaUploadSerializer,CompanyBlogSerializer

# Department ViewSet (10 APIs)

class DepartmentViewSet(viewsets.ModelViewSet): 
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    @action(detail=False, methods=['get'])
    def active_departments(self, request):
        departments = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(departments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        department = self.get_object()
        department.is_active = not department.is_active
        department.save()
        return Response({'is_active': department.is_active})

    @action(detail=False, methods=['get'])
    def recent_departments(self, request):
        departments = self.queryset.order_by('-created_at')[:5]
        serializer = self.get_serializer(departments, many=True)
        return Response(serializer.data)
    


# Employee ViewSet (10 APIs)
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @action(detail=False, methods=['get'])
    def active_employees(self, request):
        employees = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(employees, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        employee = self.get_object()
        employee.is_active = not employee.is_active
        employee.save()
        return Response({'is_active': employee.is_active})

    @action(detail=False, methods=['get'])
    def high_salary_employees(self, request):
        employees = self.queryset.filter(salary__gt=50000)
        serializer = self.get_serializer(employees, many=True)
        return Response(serializer.data)

# Project ViewSet (10 APIs)
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=False, methods=['get'])
    def ongoing_projects(self, request):
        projects = self.queryset.filter(is_completed=False)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        project = self.get_object()
        project.is_completed = True
        project.save()
        return Response({'is_completed': project.is_completed})

    @action(detail=False, methods=['get'])
    def high_budget_projects(self, request):
        projects = self.queryset.filter(budget__gt=100000)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

# Task ViewSet (10 APIs)
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=False, methods=['get'])
    def pending_tasks(self, request):
        tasks = self.queryset.filter(status='pending')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        task = self.get_object()
        task.status = 'completed'
        task.save()
        return Response({'status': task.status})

    @action(detail=False, methods=['get'])
    def overdue_tasks(self, request):
        from datetime import date
        tasks = self.queryset.filter(due_date__lt=date.today(), status__in=['pending', 'in_progress'])
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

# Client ViewSet (10 APIs)
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(detail=False, methods=['get'])
    def recent_clients(self, request):
        clients = self.queryset.order_by('-created_at')[:5]
        serializer = self.get_serializer(clients, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_contact(self, request, pk=None):
        client = self.get_object()
        client.phone = request.data.get('phone', client.phone)
        client.email = request.data.get('email', client.email)
        client.save()
        return Response({'phone': client.phone, 'email': client.email})

    @action(detail=False, methods=['get'])
    def by_company(self, request):
        company_name = request.query_params.get('company_name', None)
        if company_name:
            clients = self.queryset.filter(company_name__icontains=company_name)
            serializer = self.get_serializer(clients, many=True)
            return Response(serializer.data)
        return Response({'error': 'company_name parameter is required'}, status=400)
    
    
     
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    @action(detail=False, methods=['post'])
    def createcompany(self, request): 
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Company created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class CompanyBlogViewSet(viewsets.ModelViewSet):
    queryset = CompanyBlog.objects.all()
    serializer_class = CompanyBlogSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
class MediaUploadViewSet(viewsets.ModelViewSet):
    queryset = MediaUpload.objects.all()
    serializer_class = MediaUploadSerializer

    def get_serializer_context(self):
        return {'request': self.request}