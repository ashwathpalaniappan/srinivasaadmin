from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('changeimg', views.changeimg, name='changeimg'),
    path('oldorders', views.oldorders, name='oldorders'),
    path('currorders', views.currorders, name='currorders'),
    path('delorders', views.delorders, name='delorders'),
    path('order/<str:orderid>', views.order, name='order'),
    path('cancelorder/<str:orderid>', views.cancelorder, name='cancelorder'),
]