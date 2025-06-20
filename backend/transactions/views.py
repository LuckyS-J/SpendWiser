from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import TransactionSerializer
from .models import Transaction
import json
from django.conf import settings
from datetime import datetime
from .utils import assign_category
from django.views import View
from .forms import TransactionForm
from django.db.models import Sum
from django.db.models.functions import TruncWeek
from datetime import timedelta
from .utils import CATEGORY_KEYWORDS

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


class TransactionListView(View):
    def get(self, request):

        transactions = Transaction.objects.filter(user=request.user)
        categories = Transaction.CATEGORY_CHOICES

        category = request.GET.get('category')
        sort = request.GET.get('sort', '-date')
        transaction_type = request.GET.get('type')

        if transaction_type in ['expense', 'income']:
            transactions = transactions.filter(type=transaction_type)

        if category:
            transactions = transactions.filter(category=category)

        allowed_sort_fields = ['date', '-date', 'amount', '-amount']
        if sort in allowed_sort_fields:
            transactions = transactions.order_by(sort)

        return render(request, 'transactions/transactions_list.html', {
            'transactions': transactions,
            'categories': categories
        })


class TransactionDetailsView(View):

    def get(self, request, id):
        transaction = get_object_or_404(Transaction, id=id, user=request.user)

        return render(request, 'transactions/transaction_details.html', {
            'transaction': transaction
        })


class TransactionEditView(View):
    def get(self, request, id):
        transaction = get_object_or_404(Transaction, id=id, user=request.user)
        form = TransactionForm(instance=transaction)
        return render(request, 'transactions/transaction_edit.html', {
            'transaction': transaction,
            'form': form
        })

    def post(self, request, id):
        transaction = get_object_or_404(Transaction, id=id, user=request.user)
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transactions-list')

        return render(request, 'transactions/transaction_edit.html', {
            'form': form,
            'transaction': transaction
        })


class DeleteTransactionView(View):
    def post(self, request, id):
        transaction = get_object_or_404(Transaction, id=id, user=request.user)
        transaction.delete()
        return redirect('transactions-list')


class AddTransactionView(View):
    def get(self, request):
        form = TransactionForm()
        return render(request, 'transactions/transaction_edit.html', {
            'form': form
        })

    def post(self, request):
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transactions-list')
        return render(request, 'transactions/transaction_edit.html', {'form': form})

class ChartsView(View):
    def get(self, request):
        user = request.user

        category_data = (
            Transaction.objects.filter(user=user, type='expense')
            .values('category')
            .annotate(total=Sum('amount'))
        )

        weekly_data = (
            Transaction.objects.filter(user=user, type='expense')
            .annotate(week=TruncWeek('date'))
            .values('week')
            .annotate(total=Sum('amount'))
            .order_by('week')
        )

        def format_week_range(week_start):
            week_end = week_start + timedelta(days=6)
            return f"{week_start.strftime('%d')}–{week_end.strftime('%d %b')}"

        context = {
            'category_labels': [c['category'].capitalize() for c in category_data],
            'category_values': [float(c['total']) for c in category_data],
            'category_colors': [
                CATEGORY_KEYWORDS.get(c['category'], {}).get('color', '#cccccc') for c in category_data
            ],
            'date_labels': [format_week_range(entry['week']) for entry in weekly_data],
            'date_values': [float(entry['total']) for entry in weekly_data],
        }

        return render(request, 'transactions/charts.html', context)
