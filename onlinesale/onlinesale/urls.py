"""onlinesale URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from adminapp import views,utils

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',TemplateView.as_view(template_name='index.html')),
    path('login/',views.logincheck,name='login'),
    path('addmerchant/',views.addMerchant,name = 'addmerchant'),
    path('savemerchant/',views.saveMerchant,name='savemerchant'),
    path('deletemerchant<int:merchantid>/',views.deleteMerchant,name = 'deletemerchant'),
    path('merchantlogin/',views.MerchantLogin.as_view()),
    path('viewproduct/<int:merchantid>/',views.ViewProduct.as_view()),
    path('saveproduct/',views.SaveProduct.as_view()),
    path('deleteproduct/<int:productid>/',views.SaveProduct.as_view()),
    path('showproduct/<int:productid>/',views.SaveProduct.as_view()),
    path('updateproduct/<int:productid>/',views.SaveProduct.as_view()),
    path('updatpassword/<str:mail>/',views.ChangePassword.as_view())
]
