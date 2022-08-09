from django.urls import path
from .views import *

urlpatterns = [
    path('post_data_csv', SaveCSVTransactionData.as_view()),
    path('post_data', PostTransactionData.as_view()),
    path('records', GetTransactionData.as_view()),
    path('banks', GetUniqueBanksData.as_view()),
    path('transaction', GetTransactionsIntervalData.as_view()),
    path('customer_names', GetCustomersData.as_view()),
    path('transactions_summary', GetTransactionsSummaryData.as_view()),
    path('transaction_amount_summary', GetTransactionsAmountSummaryData.as_view()),
    path('total_transaction_amount', GetTotalTransactionsAmountSummaryData.as_view()),
]
