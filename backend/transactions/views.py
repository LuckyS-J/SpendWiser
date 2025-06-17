from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import TransactionSerializer
from .models import Transaction
import json
from django.conf import settings
from datetime import datetime
from .utils import assign_category

# Create your views here.


class TransactionListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        data = request.data.copy()

        if not data.get('category'):
            data['category'] = assign_category(data.get('title'))

        date_str = data.get('date', datetime.today().strftime('%Y-%m-%d'))

        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'date': ['Invalid date format, expected YYYY-MM-DD']}, status=400)

        existing = Transaction.objects.filter(
            user=request.user,
            title=data.get('title'),
            amount=data.get('amount'),
            date=date_obj
        ).exists()

        if existing:
            return Response({'detail': 'Transaction already exists.'}, status=400)

        data['date'] = date_obj
        type = 'income' if int(data['amount']) >= 0 else 'expense'

        print(data)

        serializer = TransactionSerializer(data=data)

        if serializer.is_valid():
            serializer.save(user=request.user, type=type)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TransactionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        transaction = get_object_or_404(Transaction, user=request.user, id=id)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=200)

    def put(self, request, id):
        transaction = get_object_or_404(Transaction, user=request.user, id=id)
        serializer = TransactionSerializer(
            instance=transaction, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        transaction = get_object_or_404(Transaction, user=request.user, id=id)
        transaction.delete()
        return Response({'message': 'Transaction deleted'}, status=204)


class ImportTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            with open(f'{settings.BASE_DIR}/data/sample_transactions.json', encoding='utf-8') as file:
                data = json.load(file)

                count = 0
                for transaction in data['transactions']:
                    date_str = transaction['date']
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

                    existing = Transaction.objects.filter(
                        user=request.user,
                        title=transaction['description'],
                        amount=transaction['amount'],
                        date=date_obj
                    ).exists()

                    if not existing:
                        category = assign_category(transaction['description'])
                        new_transaction = Transaction(
                            user=request.user,
                            title=transaction['description'],
                            amount=transaction['amount'],
                            date=date_obj,
                            category=category,
                            type='income' if transaction['amount'] >= 0 else 'expense',
                        )
                        new_transaction.save()
                        count += 1
                return Response({'Message': f'Successfully loaded {count} transactions'}, status=201)

        except FileNotFoundError:
            return Response({'Message': 'File not found'}, status=404)
