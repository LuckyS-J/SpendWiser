from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import CustomRegisterForm, CustomLoginForm, SyncCSVForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from transactions.models import Transaction
from transactions.utils import assign_category
from django.db.models import Sum
import csv
import io
from datetime import datetime

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
        serializer = UserProfileSerializer(
            instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

# ----------------------------------------#


class HomeView(LoginRequiredMixin, View):

    def get(self, request):

        balance = (
            Transaction.objects.filter(user=request.user).aggregate(
                total=Sum('amount'))['total'] or 0.0
        )

        transactions = (
            Transaction.objects.filter(user=request.user).order_by('-date')[:5]
        )

        return render(request, 'core/index.html', {
            'balance': balance,
            'transactions': transactions
        })


class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    form_class = CustomLoginForm


class CustomRegisterView(CreateView):
    form_class = CustomRegisterForm
    template_name = 'core/register.html'
    success_url = reverse_lazy('login')


class SyncView(View):
    def get(self, request):
        form = SyncCSVForm()
        return render(request, 'core/sync.html', {'form': form})

    def post(self, request):
        form = SyncCSVForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.cleaned_data['file']
            decoded_file = file.read().decode('utf-8')
            csv_file = io.StringIO(decoded_file)
            reader = csv.DictReader(csv_file)

            for row in reader:
                title = row['title']
                amount = float(row['amount'])
                date_str = row['date']

                type = 'income' if amount >= 0 else 'expense'
                category = assign_category(title)

                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    date_obj = datetime.today().date()

                exists = Transaction.objects.filter(
                    user=request.user,
                    title=title,
                    amount=amount,
                    date=date_obj,
                    type=type
                ).exists()

                if not exists:
                    Transaction.objects.create(
                        user=request.user,
                        title=title,
                        amount=amount,
                        date=date_obj,
                        category=category,
                        type=type
                    )

            return redirect('transactions-list')

        return render(request, 'core/sync.html', {'form': form})
