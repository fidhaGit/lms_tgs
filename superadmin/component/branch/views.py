from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Branch
from .serializers import BranchSerializer


class BranchListCreateView(generics.ListCreateAPIView):
    queryset = Branch.objects.filter(is_delete=False)
    serializer_class = BranchSerializer


class BranchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Branch.objects.filter(is_delete=False)
    serializer_class = BranchSerializer