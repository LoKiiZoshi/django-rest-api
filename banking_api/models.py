from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Account(models.Model):
    ACCOUNT_TYPES = (
        ('SAVINGS', 'Savings'),
        ('CHECKING', 'Checking'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_number} ({self.account_type})"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('TRANSFER', 'Transfer'),
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    recipient_account = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL, related_name='received_transactions')

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} on {self.timestamp}"

class Loan(models.Model):
    LOAN_STATUSES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, choices=LOAN_STATUSES, default='PENDING')
    applied_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Loan of {self.amount} for {self.user.username}"