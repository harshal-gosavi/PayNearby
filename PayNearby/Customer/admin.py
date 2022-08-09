from django.contrib import admin
from .models import *


# Register your models here.

class TransactionClass(admin.ModelAdmin):
    list_display = ('txn_date', 'account_holder', 'bank', 'transaction_type', 'amount')


admin.site.register(Transaction, TransactionClass)
