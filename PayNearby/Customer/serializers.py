from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'rrn', 'txn_date', 'txn', 'xxxx_number', 'account_number', 'bank', 'account_holder', 'transaction_type',
            'amount')


class BanksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('bank',)


class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('account_holder',)
