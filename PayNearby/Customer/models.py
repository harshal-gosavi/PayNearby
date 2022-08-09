from django.db import models


# Create your models here.
class Transaction(models.Model):
    rrn = models.BigIntegerField(primary_key=True)
    txn_date = models.DateTimeField(blank=True, null=True)
    txn = models.CharField(max_length=5, null=True, blank=True)
    xxxx_number = models.CharField(max_length=10, null=True, blank=True)
    account_number = models.BigIntegerField(null=True, blank=True)
    bank = models.CharField(max_length=100, null=True, blank=True)
    account_holder = models.CharField(max_length=100, null=True, blank=True)
    transaction_type = models.CharField(max_length=50, null=True, blank=True)
    amount = models.FloatField(blank=True, null=True)

    # Audit logs
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.rrn)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transaction'
