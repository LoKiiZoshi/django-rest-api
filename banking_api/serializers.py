from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account, Transaction, Loan
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        Token.objects.create(user=user)
        return user

class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'user', 'account_number', 'account_type', 'balance', 'is_active', 'created_at']

class TransactionSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    recipient_account = AccountSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'account', 'transaction_type', 'amount', 'description', 'timestamp', 'recipient_account']

class TransactionCreateSerializer(serializers.ModelSerializer):
    recipient_account_number = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = Transaction
        fields = ['transaction_type', 'amount', 'description', 'recipient_account_number']

    def validate(self, data):
        if data['transaction_type'] == 'TRANSFER' and not data.get('recipient_account_number'):
            raise serializers.ValidationError("Recipient account number is required for transfers.")
        return data

class LoanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Loan
        fields = ['id', 'user', 'amount', 'interest_rate', 'status', 'applied_at', 'approved_at']
