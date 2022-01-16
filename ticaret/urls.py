"""ticaret URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.signIn,name="home"),
    path('postsign/',views.postsign),
    path('logout/',views.logout,name="logout"),
    path('addproduce/',views.addproduce,name="addproduce"),
    path('addProduce/',views.addProduce),
    path('addcustomer/',views.addcustomer,name="addcustomer"),
    path('addCustomer/',views.addCustomer),
    path('selectcustomer/',views.selectcustomer,name="selectcustomer"),
    path('checkproduce/',views.checkproduce,name="checkproduce"),
    path('checkcustomer/',views.showcustomer,name="customers"),
    path('checkbills/',views.checkbills,name="checkbills"),
    path('checkspecialbill/',views.checkspecialbill),
    path('updatestock/',views.updatestock),
    path('updatestockk/',views.updatestockk),
    path('selectproduce/',views.selectproduce,name="selectproduce"),
    path('addproducelist/',views.addproducelist,name="addproducelist"),
    path('confirmorder/',views.confirmorder,name="confirmorder"),
    path('clearorderproductlist/',views.clearorderproductlist,name="clearorderproductslist")
]


urlpatterns+=staticfiles_urlpatterns()