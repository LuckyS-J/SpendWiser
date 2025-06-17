from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import TransactionSerializer
from .models import Transaction

# Create your views here.


class TransactionListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
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
        serializer = TransactionSerializer(instance=transaction, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, id):
        transaction = get_object_or_404(Transaction, user=request.user, id=id)
        transaction.delete()
        return Response({'message':'Transaction deleted'}, status=204)
