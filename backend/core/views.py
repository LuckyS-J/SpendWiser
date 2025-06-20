from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import CustomRegisterForm, CustomLoginForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from transactions.models import Transaction
from django.db.models import Sum

# Create your views here.


class ApiRegisterView(APIView):

    def post(self, request):

        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created'}, status=201)
        else:
            return Response(serializer.errors, status=400)
        
class ApiProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=200)

    def put(self, request):
        serializer = UserProfileSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
        
#----------------------------------------#

class HomeView(LoginRequiredMixin, View):

    def get(self, request):
        
        balance = (
            Transaction.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0.0
        )

        transactions = (
            Transaction.objects.filter(user=request.user).order_by('-date')[:5]
        )

        return render(request, 'core/index.html',{
            'balance':balance,
            'transactions':transactions
        })
    
class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    form_class = CustomLoginForm

class CustomRegisterView(CreateView):
    form_class = CustomRegisterForm
    template_name = 'core/register.html'
    success_url = reverse_lazy('login')


