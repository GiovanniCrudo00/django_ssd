from django.shortcuts import render
from rest_framework import viewsets, permissions
from records.models import Record
from records.serializers import RecordSerializer


# Create your views here.
class CustomPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser:  # Allow Read/Write permissions if superuser
                return True
            elif request.user.groups.filter(name='records_editors').exists():  # Allow Read/Write permissions if editor
                return True
            elif request.user.groups.filter(name='common_user').exists():  # Allow ReadOnly permissions if common_user
                if request.method in permissions.SAFE_METHODS:  # Only GET, HEAD, OPTIONS methods allowed
                    return True
                else:
                    return False
            else:
                return False


class RecordViewSet(viewsets.ModelViewSet):
    permission_classes = [CustomPermissions]
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    