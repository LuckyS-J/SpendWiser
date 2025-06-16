from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer

# Create your views here.


class ApiRegisterView(APIView):

    def post(self, request):

        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created'}, status=201)
        else:
            return Response(serializer.errors, status=400)
