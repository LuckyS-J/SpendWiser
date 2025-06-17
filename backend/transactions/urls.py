from django.urls import path
from .views import TransactionDetailView, TransactionListCreateView, ImportTransactionView

urlpatterns = [
    path('', TransactionListCreateView.as_view(), name='transaction-list'),
    path('<int:id>', TransactionDetailView.as_view(), name='transaction-details'),
    path('import/', ImportTransactionView.as_view(), name='transaction-import')
]