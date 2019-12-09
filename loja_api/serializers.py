from rest_framework import serializers
from django.contrib.auth.models import User
from loja_api.models import *

# Irão existir dois grupos de serializer, sendo que cada serializer possui sua versão para listagem onde pode
# se criar novas instancias e outra para detalhes onde ocorre as alterações e exclusões.
# O primeiro grupo se refere somente a acesso exclusivo do Admin onde ele pode ter o retorno de todas as informações
# de forma clara alterar quase todas infomações apenas não podendo alterar alguns dados do usuario externo
# O segundo se da ao serializer que irão ser utilizados pelos usuarios externos sendo que o usuario não autenticado
# podera somente ler

################################################################################################################################################

#class InforList(serializers.HyperlinkedModelSerializer):
#    name = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
#    class Meta:
#        model = InformacoesUsuario
#        fields = ('pk', 'name', 'address', 'telephone', 'cpf', 'cep', 'url')

################################################################################################################################################

class UserList(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'password', 'url')

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username já cadastrado")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email já cadastrado")
        return data

class AdminUserList(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'password', 'is_superuser', 'is_staff', 'is_active', 'url')
    
    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username já cadastrado")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email já cadastrado")
        return data

class AdminUserDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'password')

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username já cadastrado")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email já cadastrado")
        return data
    
class AdminOutherDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'is_superuser', 'is_staff', 'is_active')

class UserDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'password')

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username já cadastrado")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email já cadastrado")
        return data

################################################################################################################################################

class ItemList(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('name', 'value', 'url')

class ItemDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('pk', 'name', 'value', 'amount')
    
    def validate(self,data):
        item = Item.objects.get(id = data['pk'])
        if item.amount >= data['amount']:
            raise serializers.ValidationError("Itens Insuficientes em estoque.")

class AdminItemList(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField(queryset=Categoria.objects.all(), slug_field='name')
    class Meta:
        model = Item
        fields = ('pk', 'name', 'value', 'color', 'size', 'description', 'amount', 'sold_off', 'category', 'url')

    def validate(self, data):
        if data['value'] <= 0:
            raise serializers.ValidationError("O valor do item não pode ser negativo ou igual a zero.")
        elif data['amount'] < 0:
            raise serializers.ValidationError("O quantidade de itens não pode ser menor que zero.")
        elif Item.objects.filter(name = data['name']).exists():
            raise serializers.ValidationError("Não se pode ter dois itens com mesmo nome.")
        return data

class AdminItemDetail(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField(queryset=Categoria.objects.all(), slug_field='name')
    class Meta:
        model = Item
        fields = ('name', 'value', 'color', 'size', 'description', 'amount', 'sold_off', 'category')

    def validate(self, data):
        if data['value'] <= 0:
            raise serializers.ValidationError("O valor do item não pode ser negativo ou igual a zero.")
        elif data['amount'] < 0:
            raise serializers.ValidationError("O quantidade de itens não pode ser menor que zero.")
        elif Item.objects.filter(name = data['name']).exists():
            raise serializers.ValidationError("O nome do qual deseja inserir ja existe.")
        return data

################################################################################################################################################

class CategoriaList(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Categoria
        fields = ('pk', 'name', 'description', 'url')

    def validate(self, data):
        if Categoria.objects.filter(name = data['name']).exists():
            raise serializers.ValidationError("Não se pode ter duas categorias com mesmo nome.")
        return data

class AdminCategoriaDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Categoria
        fields = ('pk', 'name', 'description')

################################################################################################################################################

class ItemPurchaseList(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ItemPurchase
        fields = ('pk', 'amount_buy', 'value_itens', 'url')

    def validate(self, data):
        if data['amount_buy'] <= 0:
            raise serializers.ValidationError("A quantidade de itens a se comprada não pode ser negativo ou igual a zero.")
        return data


class ItemPurchaseDetail(serializers.HyperlinkedModelSerializer):
    #itens = ItemSerializer(many=True, read_only=True)
    item = serializers.SlugRelatedField(queryset=Item.objects.all(), slug_field='pk')
    purchase = serializers.SlugRelatedField(queryset=Purchase.objects.all(), slug_field='pk')
    class Meta:
        model = ItemPurchase
        fields = ('pk', 'item', 'purchase', 'amount_buy', 'value_itens')
     
    def validate(self, data):
        if data['amount_buy'] <= 0:
            raise serializers.ValidationError("A quantidade de itens a se comprada não pode ser negativo ou igual a zero.")
        return data


################################################################################################################################################

class PurchaseList(serializers.HyperlinkedModelSerializer):
    userId = serializers.SlugRelatedField(queryset=ItemPurchase.objects.all(), slug_field='pk')
    class Meta:
        model = Purchase
        fields = ('pk', 'userId', 'is_open', 'freight', 'total_value', 'url')

    def validate(self, data):
        if data['freight'] <= 0:
            raise serializers.ValidationError("O frete não pode ser negativo ou igual a zero.")
        return data

class PurchaseDetail(serializers.HyperlinkedModelSerializer):
    #compra = serializers.SlugRelatedField(queryset=ItemPurchase.objects.all(), slug_field='pk')
    class Meta:
        model = Purchase
        fields = ('pk', 'userId', 'is_open', 'freight', 'total_value')
    
    def validate(self, data):
        if data['freight'] <= 0:
            raise serializers.ValidationError("O frete não pode ser negativo ou igual a zero.")
        return data

################################################################################################################################################

class CarteiraList(serializers.HyperlinkedModelSerializer):
    #userId = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    class Meta:
        model = CarteiraDigital
        fields = ('pk', 'userId', 'number_account', 'value', 'url')

class CarteiraDetail(serializers.HyperlinkedModelSerializer):
    #name = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    #number_account = serializers.SlugRelatedField(queryset=CarteiraDigital.objects.all(), slug_field='number_account')
    class Meta:
        model = CarteiraDigital
        fields = ('pk', 'userId', 'number_account', 'value')

    def validate(self, data):
        if data['value'] <= 0:
            raise serializers.ValidationError("Não é permitido valores negativos ou o valor 0.")
        return data

################################################################################################################################################

class InforList(serializers.HyperlinkedModelSerializer):
    name = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    class Meta:
        model = InformacoesUsuario
        fields = ('pk', 'name', 'address', 'telephone', 'cpf', 'cep', 'url')


class InfoUserDetail(serializers.HyperlinkedModelSerializer):
    name = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    class Meta:
        model = InformacoesUsuario
        fields = ('pk', 'name', 'address', 'telephone', 'cpf', 'cep')