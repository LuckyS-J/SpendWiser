from django.urls import path
from .views import TransactionDetailView, TransactionListCreateView

urlpatterns = [
    path('', TransactionListCreateView.as_view(), name='transaction-list'),
    path('<int:id>', TransactionDetailView.as_view(), name='transaction-details'),
]