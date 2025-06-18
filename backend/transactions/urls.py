from django.urls import path
from .views import TransactionDetailView, TransactionListCreateView, ImportTransactionView

urlpatterns = [
    path('api/', TransactionListCreateView.as_view(), name='transaction-list'),
    path('api/<int:id>', TransactionDetailView.as_view(), name='transaction-details'),
    path('api/import/', ImportTransactionView.as_view(), name='transaction-import')
]
