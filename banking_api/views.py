from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth.models import User
from .models import Account, Transaction, Loan
from .serializers import (
    UserSerializer, UserRegisterSerializer,
    AccountSerializer, TransactionSerializer, TransactionCreateSerializer,
    LoanSerializer
)
from django.db import transaction as db_transaction
import random
import string
from django.utils import timezone

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'login']:
            return [AllowAny()]
        elif self.action in ['list', 'approve_user']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        return UserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        user = User.objects.filter(username=request.data.get('username')).first()
        if user and user.check_password(request.data.get('password')):
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': UserSerializer(user).data})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['post'], url_path='approve')
    def approve_user(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'status': 'User approved'})

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.action in ['update_status', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Account.objects.all()
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        account_number = ''.join(random.choices(string.digits, k=12))
        while Account.objects.filter(account_number=account_number).exists():
            account_number = ''.join(random.choices(string.digits, k=12))
        serializer.save(user=self.request.user, account_number=account_number)

    @action(detail=True, methods=['post'], url_path='update-status')
    def update_status(self, request, pk=None):
        account = self.get_object()
        is_active = request.data.get('is_active', True)
        account.is_active = is_active
        account.save()
        return Response({'status': 'Account status updated'})

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Transaction.objects.all()
        return Transaction.objects.filter(account__user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return TransactionCreateSerializer
        return TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with db_transaction.atomic():
            account = Account.objects.filter(user=request.user, is_active=True).first()
            if not account:
                return Response({'error': 'No active account found'}, status=status.HTTP_400_BAD_REQUEST)

            transaction_type = serializer.validated_data['transaction_type']
            amount = serializer.validated_data['amount']

            if transaction_type == 'DEPOSIT':
                account.balance += amount
                account.save()
            elif transaction_type == 'WITHDRAWAL':
                if account.balance < amount:
                    return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)
                account.balance -= amount
                account.save()
            elif transaction_type == 'TRANSFER':
                recipient_account_number = serializer.validated_data.get('recipient_account_number')
                recipient = Account.objects.filter(account_number=recipient_account_number, is_active=True).first()
                if not recipient:
                    return Response({'error': 'Recipient account not found'}, status=status.HTTP_400_BAD_REQUEST)
                if account.balance < amount:
                    return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)
                account.balance -= amount
                recipient.balance += amount
                account.save()
                recipient.save()
                serializer.validated_data['recipient_account'] = recipient

            transaction = Transaction.objects.create(
                account=account,
                transaction_type=transaction_type,
                amount=amount,
                description=serializer.validated_data.get('description', '')
            )
            return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def get_permissions(self):
        if self.action == 'approve_loan':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Loan.objects.all()
        return Loan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, interest_rate=Decimal('5.00'))

    @action(detail=True, methods=['post'], url_path='approve')
    def approve_loan(self, request, pk=None):
        loan = self.get_object()
        status = request.data.get('status', 'APPROVED')
        if status not in ['APPROVED', 'REJECTED']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        loan.status = status
        if status == 'APPROVED':
            loan.approved_at = timezone.now()
        loan.save()
        return Response({'status': f'Loan {status.lower()}'})