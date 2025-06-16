from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Sum, Avg
from datetime import date, timedelta
from .models import *
from .serializers import *

class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'address', 'librarian']
    ordering_fields = ['name', 'established_date']

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        library = self.get_object()
        stats = {
            'total_books': library.books.count(),
            'available_books': library.books.filter(is_available=True).count(),
            'total_members': library.members.count(),
            'active_members': library.members.filter(is_active=True).count(),
            'books_issued': BookIssue.objects.filter(book__library=library, status='ISSUED').count(),
            'overdue_books': BookIssue.objects.filter(book__library=library, status='OVERDUE').count(),
        }
        return Response(stats)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'nationality']
    ordering_fields = ['first_name', 'last_name', 'birth_date']

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'established_year']

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'publisher', 'library', 'condition', 'is_available', 'language']
    search_fields = ['title', 'isbn', 'authors__first_name', 'authors__last_name']
    ordering_fields = ['title', 'publication_date', 'created_at']

    @action(detail=False, methods=['get'])
    def popular(self, request):
        popular_books = Book.objects.annotate(
            issue_count=Count('book_issues')
        ).order_by('-issue_count')[:10]
        serializer = self.get_serializer(popular_books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def available(self, request):
        available_books = Book.objects.filter(is_available=True, available_quantity__gt=0)
        page = self.paginate_queryset(available_books)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(available_books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reserve(self, request, pk=None):
        book = self.get_object()
        member_id = request.data.get('member_id')
        
        try:
            member = Member.objects.get(id=member_id)
            
            # Check if book is available
            if not book.is_available:
                return Response({'error': 'Book is not available'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if member already has a reservation for this book
            existing_reservation = Reservation.objects.filter(
                book=book, member=member, status='ACTIVE'
            ).exists()
            
            if existing_reservation:
                return Response({'error': 'Member already has an active reservation for this book'}, 
                              status=status.HTTP_409_CONFLICT)
            
            reservation = Reservation.objects.create(
                book=book,
                member=member
            )
            
            serializer = ReservationSerializer(reservation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['library', 'membership_type', 'gender', 'is_active']
    search_fields = ['first_name', 'last_name', 'member_id', 'email']
    ordering_fields = ['first_name', 'last_name', 'membership_date']

    @action(detail=True, methods=['get'])
    def issued_books(self, request, pk=None):
        member = self.get_object()
        issued_books = BookIssue.objects.filter(member=member, status__in=['ISSUED', 'OVERDUE'])
        serializer = BookIssueSerializer(issued_books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        member = self.get_object()
        history = BookIssue.objects.filter(member=member).order_by('-issued_date')
        page = self.paginate_queryset(history)
        if page is not None:
            serializer = BookIssueSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = BookIssueSerializer(history, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def fines(self, request, pk=None):
        member = self.get_object()
        fines = Fine.objects.filter(member=member)
        serializer = FineSerializer(fines, many=True)
        return Response(serializer.data)

class BookIssueViewSet(viewsets.ModelViewSet):
    queryset = BookIssue.objects.all()
    serializer_class = BookIssueSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['book', 'member', 'status', 'issued_by']
    search_fields = ['book__title', 'member__first_name', 'member__last_name']
    ordering_fields = ['issued_date', 'due_date']

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        issue = self.get_object()
        
        if issue.status == 'RETURNED':
            return Response({'error': 'Book already returned'}, status=status.HTTP_400_BAD_REQUEST)
        
        issue.status = 'RETURNED'
        issue.return_date = date.today()
        issue.returned_by = request.user
        issue.save()
        
        # Update book availability
        book = issue.book
        book.available_quantity += 1
        book.save()
        
        # Calculate fine if overdue
        if issue.days_overdue > 0:
            fine_amount = issue.days_overdue * 1.00  # $1 per day
            Fine.objects.create(
                member=issue.member,
                book_issue=issue,
                fine_type='OVERDUE',
                amount=fine_amount,
                description=f"Overdue fine for '{issue.book.title}' - {issue.days_overdue} days late",
                due_date=date.today() + timedelta(days=30)
            )
        
        serializer = self.get_serializer(issue)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        overdue_issues = BookIssue.objects.filter(
            status='ISSUED',
            due_date__lt=date.today()
        )
        # Update status to overdue
        overdue_issues.update(status='OVERDUE')
        
        serializer = self.get_serializer(overdue_issues, many=True)
        return Response(serializer.data)

