from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import *
from rest_framework import filters
from loja_api.models import *
from loja_api.serializers import *
from loja_api.permissions import *
import random

# As views tbm irão ser de dois grupos seguindo os padrões anteriores de divisão, uma parte para o admin e outros para
# usuários externos, aki teremos alguns tratamentos em relação aos dados que irão ser passados ja que devem se gerados
# de forma automatica

#########################################################################################################################

class UserListView(generics.ListCreateAPIView):
    permission_classes = (UserListPermission,)
    name = 'user-list'

    def perform_create(self, serializer):
        if User.objects.filter(is_superuser=True).exists():
            nome = serializer.validated_data['username']
            email = serializer.validated_data['email']
            senha = serializer.validated_data['password']
            usuario = User.objects.create_user(nome, email = email, password = senha)
            usuario.is_staff = True
            usuario.is_superuser = False
            usuario.save()
            numero = random.randint(0,10000000)
            carteira = CarteiraDigital.objects.create(userId = usuario, number_account = numero, value = 0)
            compra = Purchase.objects.create(userId = usuario, is_open = True, freight = 0, total_value = 0)
            carteira.save()
            compra.save()
            
        else:
            nome = serializer.validated_data['username']
            email = serializer.validated_data['email']
            senha = serializer.validated_data['password']
            usuario = User.objects.create_user(nome, email = email, password = senha)
            usuario.is_staff = True
            usuario.is_superuser = True
            usuario.save()
            numero = random.randint(0,100000000)
            carteira = CarteiraDigital.objects.create(userId = usuario, number_account = numero, value = 0)
            compra = Purchase.objects.create(userId = usuario, is_open = True, freight = 0, total_value = 0)
            carteira.save()
            compra.save()
            

    def get_queryset(self):
        user = self.request.user
        
        if user.is_superuser:
            return User.objects.all()
        
        elif user.id == None:
            return []

        else:
            return User.objects.filter(id = user.id)

    def get_serializer_class(self):
        user = self.request.user
        
        if user.is_superuser:
            return AdminUserList
        else:
            return UserList

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (UserDetailPermission,)
    queryset = User.objects.all()
    name = 'user-detail'

    def get_serializer_class(self):
        user = self.request.user
        id = self.kwargs['pk']

        if user.is_superuser:
            if user.id == id:
                return AdminUserDetail
            else:
                return AdminOutherDetail
        else:
            return UserDetail
    
    def perform_update(self, serializer):
        user_atual = self.request.user
        user = User.objects.get(id = serializer.validated_data['pk'])

        if user_atual.is_superuser:
            if self.lookup_field == user.id:
                user.username = serializer.validated_data['username']
                user.email = serializer.validated_data['email']
                user.set_password(serializer.validated_data['password'])
                user.save()
            else:
                user.is_staff = serializer.validated_data['is_staff']
                user.is_active = serializer.validated_data['is_active']
                user.is_superuser = serializer.validated_data['is_superuser']
                user.save()
        else:
            user.username = serializer.validated_data['username']
            user.email = serializer.validated_data['email']
            user.set_password(serializer.validated_data['password'])
            user.save()

########################################################################################################################

class CategoriaListView(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    permission_classes = (CategoriaFullPermission,)
    serializer_class = CategoriaList
    name = 'categoria-list'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']

class CategoriaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    permission_classes = (CategoriaFullPermission,)
    serializer_class = AdminCategoriaDetail
    name = 'categoria-detail'

########################################################################################################################

class ItemListView(generics.ListCreateAPIView):
    name = 'item-list'
    permission_classes=(ItemFullPermission,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'value']
    search_fields = ['name', 'value']
    ordering_fields = ['name', 'value', 'amount']

    def perform_create(self, serializer):
        quantidade = serializer.validated_data['amount']
        serializer.save(sold_off = False)
        if quantidade == 0:
            serializer.save(sold_off = True)
    
    def get_serializer_class(self):
        user = self.request.user

        if user.is_superuser:
            return AdminItemList
        else:
            return ItemList

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Item.objects.all()
        else:
            return Item.objects.filter(sold_off = False)
         
class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (ItemFullPermission,)
    queryset = Item.objects.all()
    name = 'item-detail'

    def get_serializer_class(self):
        user = self.request.user

        if user.is_superuser:
            return AdminItemDetail
        else:
            return ItemDetail
    
    def perform_update(self, serializer):
        user = self.request.user
        item = Item.objects.get(id = serializer.validated_data['pk'])

        if not user.is_superuser:
            nova_quatidade = item.amount - serializer.validated_data['amount']
            if nova_quatidade == 0:
                item.amount = nova_quatidade
                item.value = item.value
                item.name = item.name
                item.sold_off == True
                item.save()
                compra = Purchase.objects.get(userId = user, is_open=True)
                carrinho = ItemPurchase.objects.create(item = item, purchase = compra, amount_buy = serializer.validated_data['amount'], value = (serializer.validated_data['amount']*item.value))
                carrinho.save()
            else:
                item.name = item.name
                item.value = item.value
                item.amount = nova_quatidade
                item.save()
                compra = Purchase.objects.get(userId = user, is_open=True)
                carrinho = ItemPurchase.objects.create(item = item, purchase = compra, amount_buy = serializer.validated_data['amount'], value = (serializer.validated_data['amount']*item.value))
                carrinho.save()

        else:
            nova_quatidade = item.amount + serializer.validated_data['amount']
            if serializer.validated_data['sold_off'] == True:
                item.name = serializer.validated_data['name']
                item.value = serializer.validated_data['value']
                item.color = serializer.validated_data['sicolorze']
                item.size = serializer.validated_data['size']
                item.description = serializer.validated_data['description']
                item.amount = 0
                item.sold_off = True
                item.save()
            else:
                item.name = serializer.validated_data['name']
                item.value = serializer.validated_data['value']
                item.color = serializer.validated_data['sicolorze']
                item.size = serializer.validated_data['size']
                item.description = serializer.validated_data['description']
                item.amount = nova_quatidade
                item.sold_off = item.sold_off
                item.save()

########################################################################################################################

class PurchasesListView(generics.ListAPIView):
    serializer_class = PurchaseList
    name = 'purchase-list'
    permission_classes = (PurchaseFullPermission,)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Purchase.objects.all()
        else:
            return Purchase.objects.filter(userId = user.id)

class PurchasesDetailView(generics.RetrieveUpdateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseDetail
    name = 'purchase-detail'
    permission_classes = (PurchaseFullPermission,)

    def perform_update(self, serializer):
        compra = Purchase.objects.get(id = serializer.validated_data['pk'])
        compra.userId = compra.userId
        if serializer.validated_data['is_open'] == False:
            carteira = CarteiraDigital.objects.get(id= self.request.user.id)
            if (carteira.value - compra.total_value) >= 0:    
                nova_compra = Purchase.objects.create(userId = usuario, is_open = True, freight = 0, total_value = 0)
                nova_compra.save()
                compra.is_open = False
                carteira.value = carteira.value - compra.total_value
                carteira.save()
                compra.save()
            
        else:
            compra.is_open = True
            compra.freight = serializer.validated_data['freight']
            compra.total_value = compra.total_value
            compra.save()

########################################################################################################################

class InfoListView(generics.ListCreateAPIView):
    queryset = InformacoesUsuario.objects.all()
    serializer_class = InforList
    name = 'infoUser-list'
    permission_classes = (InfoFullPermission,)

class InfoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InformacoesUsuario.objects.all()
    serializer_class = InfoUserDetail
    name = 'infoUser-detail'
    permission_classes = (InfoFullPermission,)

########################################################################################################################

class CarteiraListView(generics.ListCreateAPIView):
    permission_classes = (UserListPermission,)
    serializer_class = CarteiraList
    name = 'carteiradigital-list'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['number_account']
    search_fields = ['number_account']
    ordering_fields = ['number_account']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return CarteiraDigital.objects.all()
        else:
            return CarteiraDigital.objects.filter(userId = user.id)

class CarteiraDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (UserListPermission,)
    queryset = CarteiraDigital.objects.all()
    serializer_class = CarteiraDetail
    name = 'carteiradigital-detail'


########################################################################################################################

class ItemPurchaseListView(generics.ListCreateAPIView):
    serializer_class = ItemPurchaseList
    name = 'itemPurchase-list'
    permission_classes = (ItemPurFullPermission,)

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return ItemPurchase.objects.all()
        else:
            compra = Purchase.objects.get(userId = user.id, is_open = True)
            return ItemPurchase.objects.filter(purchase = compra.id)

class ItemPurchaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ItemPurchase.objects.all()
    serializer_class = ItemPurchaseDetail
    name = 'itempurchase-detail'
    permission_classes = (ItemPurFullPermission,)

    def perform_update(self, serializer):
        carrinho = ItemPurchaseDetail.objects.get(id = serializer.validated_data['pk'])
        if serializer.validated_data['amount_buy'] == 0:
            item = Item.ojects.get(id = carrinho.item.id)
            compra = Purchase.objects.get(id = carrinho.purchase.id)
            valor_compra = carrinho.amount_buy * item.value
            item.amount = item.amount + carrinho.amount_buy
            compra.total_value = compra.total_value - valor_compra
            item.save()
            carrinho.delete()
            compra.save()
            
        else:
            item = Item.ojects.get(id = carrinho.item.id)
            compra = Purchase.objects.get(id = carrinho.purchase.id)
            novo_valor = item.valor * serializer.validated_data['amount_buy']
            restaurar = carrinho.amount_buy - serializer.validated_data['amount_buy']
            valor_compra = restaurar * item.value
            carrinho.amount_buy = carrinho.amount_buy + restaurar
            carrinho.value_itens = carrinho.value_itens + novo_valor 
            carrinho.amount_buy = serializer.validated_data['amount_buy']
            item.amount = item.amount + restaurar
            compra.total_value = compra.total_value + valor_compra
            carrinho.save()
            item.save()
            compra.save()

################################################# ROOT ########################################################

class InicioView(generics.GenericAPIView):
    name = 'inicio'
    def get(self, request):
        if request.user.is_superuser:
            return Response({
                'entidades' : reverse('entidades-list', request=request),
            })
            
        elif request.user.id == None:
            return Response({
                'Lita-Itens' : reverse('item-list', request=request),
                'Cadastrar' : reverse('user-list', request=request),
            })

        elif len(User.objects.all()) == 0:
            return Response({
                'Cadastrar-Admin' : reverse('user-list', request=request),
            })
        
        else:
            return Response({
                'Categorias' : reverse('categoria-list', request=request),
                'Menu-Itens': reverse('item-list',request=request),
                'Historico-Compras': reverse('purchase-list', request=request),
                'Carrinho': reverse('itemPurchase-list', request=request),
                'Minhas-Informacoes': reverse('infoUser-list', request=request),
                'Carteira': reverse('carteiradigital-list', request=request),     
                'Meu-Perfil' : reverse('user-list', request=request),
            })


class EntidadesView(generics.GenericAPIView):
    name = 'entidades-list'
    #permission_classes = (IsAdminUser,)

    def get(self, request):
        return Response({
            'categoria' : reverse('categoria-list', request=request),
            'itens': reverse('item-list',request=request),
            'purchases': reverse('purchase-list', request=request),
            'purchase_itens': reverse('itemPurchase-list', request=request),
            'infor': reverse('infoUser-list', request=request),
            'carteira': reverse('carteiradigital-list', request=request),     
            'user' : reverse('user-list', request=request),
})