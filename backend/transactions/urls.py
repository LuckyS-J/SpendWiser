from django.urls import path
from .views import TransactionDetailView, TransactionListCreateView, ImportTransactionView, TransactionListView

urlpatterns = [
    path('api/', TransactionListCreateView.as_view(), name='transaction-list'),
    path('api/<int:id>', TransactionDetailView.as_view(), name='transaction-details'),
    path('api/import/', ImportTransactionView.as_view(), name='transaction-import'),
    path('', TransactionListView.as_view(), name='transactions-list')
]
