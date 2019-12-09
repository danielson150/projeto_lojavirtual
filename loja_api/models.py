from django.db import models

# Create your models here.
# O modelo utilizado para o trabalho consiste em uma loja virtual, nela temos 3 grupos de usuários, 1º grupo consiste
# no UserAdmin que é o usuário que utiliza a api da loja em sua aplicação e tem total acesso sobre todas as partes da api,
# no 2º grupo temos usuários externos autenticados que possuem um parte do acesso restrito
# e no 3º grupo temos usuarios externos não autenticados que so podem ler uma parte ainda menor dos dados na api
# O model possui 6 classes: a classe Categoria somente possui o atributo name, ela existe para que se possa ter um delimitador
# sobre quantas cateorias existem e tabém possa ser utilizado como um buscador;
# a classe Item se refere aos itens que irão ser vendidos;
# a classe ItemPurchase que pode ser explicada assim como o carrinho ou sacola de outras aplicações semelhantes como magazineLuiza;
# a classe Purchase que se concretiza apos se feito;
# a classe InformacoesUsuario e uma classe que ira guardadr informações da qual o User do django não armazena mas que se tornam
# necessárias para a API;
# a classe CarteiraDigital e uma classe que armazena um valor da qual será usado como crédito disponivel para efetuar compras

class Categoria(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)

class Item(models.Model):
    name = models.CharField(max_length=50)
    value = models.FloatField()
    color = models.CharField(max_length=25)
    size = models.CharField(max_length=10)
    description = models.TextField()
    amount = models.IntegerField()
    sold_off = models.BooleanField(default=False)
    category = models.ForeignKey('Categoria', verbose_name=("produtos"), on_delete=models.CASCADE)

class Purchase(models.Model):
    userId = models.ForeignKey('auth.User', verbose_name=("compras"), on_delete=models.CASCADE)
    is_open = models.BooleanField()
    freight = models.FloatField()
    total_value = models.FloatField()

class ItemPurchase(models.Model):
    item = models.ForeignKey('Item', verbose_name=("itens"), on_delete=models.CASCADE)
    purchase = models.ForeignKey('Purchase', verbose_name=("compra"), on_delete=models.CASCADE)
    amount_buy = models.IntegerField()
    value_itens = models.FloatField()


class InformacoesUsuario(models.Model):
    userId = models.OneToOneField('auth.User', related_name = "informacoes", on_delete=models.CASCADE)
    address = models.TextField(null=False, blank=False)
    telephone = models.CharField(max_length=14, null=False, blank=False)
    cpf = models.CharField(max_length=11)
    cep = models.CharField(max_length=8)

class CarteiraDigital(models.Model):
    userId = models.OneToOneField('auth.User', verbose_name=("carteira"), on_delete=models.CASCADE)
    number_account = models.IntegerField()
    value = models.FloatField()
