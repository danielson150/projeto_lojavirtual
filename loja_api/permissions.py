from rest_framework import permissions
from django.contrib.auth.models import User
from loja_api.models import *

class UserListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            if request.user.id == None:
                return True

class UserDetailPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            if request.user.is_superuser:
                return True
            if view.kwargs['pk'] == request.user.id:
                return True
        if request.method == 'PATCH':
            if view.kwargs['pk'] == request.user.id or request.user.is_superuser:
                return True

class CategoriaFullPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            if request.user.is_superuser:
                return True
        if request.method == 'PUT':
            if request.user.is_superuser:
                return True
        if request.method == 'PATCH':
            if request.user.is_superuser:
                return True

class ItemFullPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            if request.user.is_superuser:
                return True
        if request.method == 'PATCH':
            if request.user.is_staff:
                return True
        

class PurchaseFullPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            if request.user.is_staff:
                return True
        if request.method == 'POST':
            return False
        if request.method == 'PATCH':
            compra = Purchase.objects.get(id = view.kwargs['pk'])
            if compra.userId == request.user.id and compra.is_open == True:
                return True

class InfoFullPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            if request.user.is_staff:
                return True
        if request.method == 'POST':
            if request.user.is_staff:
                if not InformacoesUsuario.objects.filter(id = view.kwargs['pk']).exists():
                    return True
        if request.method == 'PATCH':
            info = InformacoesUsuario.objects.get(id = view.kwargs['pk'])
            if info.userId == request.user.id:
                return True

class CarteiraFullPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            if request.user.is_staff:
                return True
        if request.method == 'POST':
            return False
        if request.method == 'PATCH':
            carteira = CarteiraDigital.objects.get(id = view.kwargs['pk'])
            if carteira.userId == request.user.id:
                return True

class ItemPurFullPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            if request.user.is_staff:
                return True
        if request.method == 'POST':
            return False
        if request.method == 'PATCH':
            item = ItemPurchase.objects.get(id = view.kwargs['pk'])
            compra = Purchase.objects.get(id = item.purchase, is_open = True)
            if compra.userId == request.user.id:
                return True