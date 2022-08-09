import os.path
from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .pagination import CustomPaginator
from django.http.response import JsonResponse
from django.db import transaction
from django.db.models.functions import Lower
from django.db.models import Q, F, Sum, Count
from .models import Transaction
from .serializers import *
import logging
from .utility.utils import process_data, camel
import pandas as pd


# Create your views here.
class SaveCSVTransactionData(APIView):
    """
        Class Name: SaveCSVTransactionData
        Method: POST
        Parameters: file:- filename of customer data
        Description: This class is used to take customer data as csv file and process data then save it in DATABASE
    """

    @transaction.atomic
    def post(self, request, pk=None):
        try:
            requestData = request.data
            file = requestData['file']
            if file:
                path = os.path.join('resources', file)
                if os.path.exists(path):
                    df = pd.read_csv(path)
                    for index, record in df.iterrows():
                        data = record.to_dict()
                        txn_date = data.get('TXN DATE', '')
                        format = '%Y-%m-%d'
                        txn_date = datetime.strptime(txn_date, format)
                        narration = data.get('NARRATION', '')
                        amount = data.get('AMOUNT', '')
                        # Process Data
                        txn, xxxx_number, rrn, account_number, bank, account_holder, transaction_type \
                            = process_data(narration)
                        # Save Data
                        obj = Transaction(rrn=rrn.split(':')[1], txn_date=txn_date, txn=txn, xxxx_number=xxxx_number,
                                          account_number=account_number, bank=bank,
                                          account_holder=camel(account_holder),
                                          transaction_type=transaction_type, amount=amount)
                        obj.save()

                    transactions = Transaction.objects.all()
                    paginator = CustomPaginator()
                    response = paginator.generate_response(transactions, TransactionSerializer, request)
                    return JsonResponse({
                        'status': status.HTTP_200_OK,
                        'response': response.data,
                        'filter_parameters': requestData
                    })
                else:
                    logging.error("File not found")
                    return JsonResponse({
                        'status': status.HTTP_404_NOT_FOUND,
                        'response': 'File not found.'
                    })
            else:
                return JsonResponse({
                    'status': status.HTTP_422_UNPROCESSABLE_ENTITY,
                    'response': 'Require Parameter missing.'
                })
        except KeyError as e:
            print(e)
            logging.error("Save Transaction Data:{}".format(e))
            return JsonResponse({
                'status': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'response': 'Require Parameter missing.'
            })

        except Exception as e:
            print(e)
            logging.error("Save Transaction Data:{}".format(e))
            return JsonResponse({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'response': 'Internal Server Error'
            })


class PostTransactionData(APIView):
    """
        Class Name: PostTransactionData
        Method: POST
        Parameters:
                - txn_date
                - narration
                - amount
        Description: This will take the data, and saves it in the database after processing and return a successful
         response.
    """

    @transaction.atomic
    def post(self, request, pk=None):
        try:
            requestData = request.data
            txn_date = requestData['txn_date']
            narration = requestData['narration']
            amount = requestData['amount']
            format = '%Y-%m-%d'
            txn_date = datetime.strptime(txn_date, format)

            # Process Data
            txn, xxxx_number, rrn, account_number, bank, account_holder, transaction_type \
                = process_data(narration)
            # Save Data
            if Transaction.objects.filter(rrn=rrn.split(':')[1]).exists():
                return JsonResponse({
                    'status': status.HTTP_409_CONFLICT,
                    'response': 'Transaction data already exists.'
                })

            obj = Transaction(rrn=rrn.split(':')[1], txn_date=txn_date, txn=txn, xxxx_number=xxxx_number,
                              account_number=account_number, bank=bank, account_holder=camel(account_holder),
                              transaction_type=transaction_type, amount=amount)
            obj.save()

            response = TransactionSerializer(obj)
            return JsonResponse({
                'status': status.HTTP_200_OK,
                'response': response.data,
                'filter_parameters': requestData
            })

        except KeyError as e:
            print(e)
            logging.error("Save Transaction Data:{}".format(e))
            return JsonResponse({
                'status': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'response': 'Require Parameter missing.'
            })

        except Exception as e:
            print(e)
            logging.error("Save Transaction Data:{}".format(e))
            return JsonResponse({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'response': 'Internal Server Error'
            })


class GetTransactionData(ListAPIView):
    """
        Class Name: GetTransactionData
        Description: This class is used to return number of rows present in your db in json format.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = CustomPaginator


class GetUniqueBanksData(APIView):
    """
        Class Name: GetUniqueBanksData
        Method: GET
        Description: This api call should return number of unique banks present iN your db in json format.
    """

    @transaction.atomic
    def get(self, request, pk=None):
        try:
            # Unique Banks
            banks = Transaction.objects.values('bank').distinct()
            response = BanksSerializer(banks, many=True)
            return JsonResponse({
                'status': status.HTTP_200_OK,
                'response': response.data,
            })

        except Exception as e:
            print(e)
            logging.error("Get Unique Banks Data:{}".format(e))
            return JsonResponse({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'response': 'Internal Server Error'
            })


class GetTransactionsIntervalData(APIView):
    """
        Class Name: GetTransactionsIntervalData
        Method: GET
        Parameters:
                - from_date
                - to_date
        Description: This api call will take 2 query parameters as input i.e, from date and to date and will
        return number of ransactions occurred during that interval.
    """

    @transaction.atomic
    def get(self, request, pk=None):
        try:
            from_date = request.GET['from_date']
            to_date = request.GET['to_date']
            format = '%Y-%m-%d'
            # checking if format matches the date
            try:
                bool(datetime.strptime(from_date, format))
                bool(datetime.strptime(to_date, format))
            except ValueError:
                return JsonResponse({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'response': 'Bad Request. Please check your date format(yyyy-mm-dd)'
                })
            from_date = datetime.strptime(from_date, format)
            to_date = datetime.strptime(to_date, format)
            response = Transaction.objects.filter(txn_date__gte=from_date,
                                                  txn_date__lte=to_date).order_by('txn_date')
            response = TransactionSerializer(response, many=True)
            return JsonResponse({
                'status': status.HTTP_200_OK,
                'response': response.data,
            })

        except KeyError as e:
            print(e)
            logging.error("Get Transactions Interval Data:{}".format(e))
            return JsonResponse({
                'status': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'response': 'Require Parameter missing.'
            })

        except Exception as e:
            print(e)
            logging.error("Get Transactions Interval Data:{}".format(e))
            return JsonResponse({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'response': 'Internal Server Error'
            })


class GetCustomersData(APIView):
    """
        Class Name: GetCustomersData
        Method: GET
        Description: This api should return names of all customers in Camel Case format.
    """

    @transaction.atomic
    def get(self, request, pk=None):
        try:
            # Customers Names
            customers = Transaction.objects.all()
            response = CustomersSerializer(customers, many=True)
            return JsonResponse({
                'status': status.HTTP_200_OK,
                'response': response.data,
            })

        except Exception as e:
            print(e)
            logging.error("Get Customers Data:{}".format(e))
            return JsonResponse({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'response': 'Internal Server Error'
            })


class GetTransactionsSummaryData(APIView):
    """
        Class Name: GetTransactionsSummaryData
        Method: GET
        Description: This api call should return number of transactions based on its type. E.g, { ‘IMPS’ : 10, ‘NEFT’ : 15 }
    """

    @transaction.atomic
    def get(self, request, pk=None):
        try:
            result = []
            transaction_type = Transaction.objects.values('transaction_type').distinct()
            for type in transaction_type:
                type_obj = type["transaction_type"]
                count = Transaction.objects.filter(transaction_type=type_obj).count()
                data = {type_obj: count}
                result.append(data)

            return JsonResponse({
                'status': status.HTTP_200_OK,
                'response': result,
            })

        except Exception as e:
            print(e)
            logging.error("GetT ransactions Summary Data:{}".format(e))
            return JsonResponse({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'response': 'Internal Server Error'
            })


class GetTransactionsAmountSummaryData(APIView):
    """
        Class Name: GetTransactionsAmountSummaryData
        Method: GET
        Description: This api call should return total amount of transactions based on its type. E.g, { ‘IMPS’ : 12,265, ‘NEFT’ : 10,560 }
    """

    @transaction.atomic
    def get(self, request, pk=None):
        try:
            result = []
            transaction_type = Transaction.objects.values('transaction_type').distinct()
            for type in transaction_type:
                type_obj = type["transaction_type"]
                amount = Transaction.objects.filter(transaction_type=type_obj).aggregate(Sum('amount'))
                data = {type_obj: amount['amount__sum']}
                result.append(data)

            return JsonResponse({
                'status': status.HTTP_200_OK,
                'response': result,
            })

        except Exception as e:
            print(e)
            logging.error("Get Transactions Amount Summary Data:{}".format(e))
            return JsonResponse({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'response': 'Internal Server Error'
            })


class GetTotalTransactionsAmountSummaryData(APIView):
    """
        Class Name: GetTotalTransactionsAmountSummaryData
        Method: GET
        Description: This api call should return total transaction amount.
    """

    @transaction.atomic
    def get(self, request, pk=None):
        try:
            total_amount = Transaction.objects.aggregate(Sum('amount'))
            return JsonResponse({
                'status': status.HTTP_200_OK,
                'total amount': total_amount['amount__sum'],
            })

        except Exception as e:
            print(e)
            logging.error("Get Total Transactions Amount Summary Data:{}".format(e))
            return JsonResponse({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'response': 'Internal Server Error'
            })
