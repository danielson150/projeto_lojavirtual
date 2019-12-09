"""lojavirtual URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

#from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from loja_api import views
from django.contrib.auth.views import LoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
#from rest_framework_swagger.views import get_swagger_view
#schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    
    #url(r'^$', schema_view),

    path('api-auth/', LoginView.as_view(), name="login"),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

################################################################################################################################################################
    
    path('user/',views.UserListView.as_view(), name= views.UserListView.name),

    path('user/<int:pk>',views.UserDetailView.as_view(), name= views.UserDetailView.name),

    path('categorias/',views.CategoriaListView.as_view(), name= views.CategoriaListView.name),

    path('categorias/<int:pk>/',views.CategoriaDetailView.as_view(), name= views.CategoriaDetailView.name),

    path('itens/', views.ItemListView.as_view(), name= views.ItemListView.name),

    path('itens/<int:pk>', views.ItemDetailView.as_view(), name= views.ItemDetailView.name),

    path('purchases/', views.PurchasesListView.as_view(), name= views.PurchasesListView.name),

    path('purchases/<int:pk>', views.PurchasesDetailView.as_view(), name= views.PurchasesDetailView.name),

    path('purchases_itens/', views.ItemPurchaseListView.as_view(), name= views.ItemPurchaseListView.name),

    path('purchases_itens/<int:pk>', views.ItemPurchaseDetailView.as_view(), name= views.ItemPurchaseDetailView.name),

    path('info-usuario', views.InfoListView.as_view(), name= views.InfoListView.name),

    path('info-usuario/<int:pk>', views.InfoDetailView.as_view(), name= views.InfoDetailView.name),

    path('carteira/', views.CarteiraListView.as_view(), name= views.CarteiraListView.name),

    path('carteira/<int:pk>', views.CarteiraDetailView.as_view(), name= views.CarteiraDetailView.name),


################################################################################################################################################################
    
    path('entidades/', views.EntidadesView.as_view(), name= views.EntidadesView.name),

    path('', views.InicioView.as_view(), name= views.InicioView.name),

]