from django.contrib import admin
from .models import Account, Transaction, Loan

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'user', 'account_type', 'balance', 'is_active']
    search_fields = ['account_number', 'user__username']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_type', 'account', 'amount', 'timestamp']
    search_fields = ['account__account_number']

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'status', 'applied_at']
    search_fields = ['user__username']