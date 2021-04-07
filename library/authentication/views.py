from django.shortcuts import render
from rest_framework import viewsets

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):

    def list(self, request):
        pass
