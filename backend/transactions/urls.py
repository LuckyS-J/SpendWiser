from django.urls import path
from .views import TransactionDetailView, TransactionListCreateView, ImportTransactionView

urlpatterns = [
    path('transactions/api/', TransactionListCreateView.as_view(), name='transaction-list'),
    path('transactions/api/<int:id>', TransactionDetailView.as_view(), name='transaction-details'),
    path('transactions/api/import/', ImportTransactionView.as_view(), name='transaction-import')
]
