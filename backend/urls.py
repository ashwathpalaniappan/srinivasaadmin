from django.urls import path
from . import views

urlpatterns = [
    path('changeImage', views.changeImage, name='changeImage'),
    path('getOldOrders', views.getOldOrders, name='getOldOrders'),
    path('getCurrOrders', views.getCurrOrders, name='getCurrOrders'),
    path('getDelOrders', views.getDelOrders, name='getDelOrders'),
    path('delivery', views.delivery, name='delivery'),
    path('cancelorder', views.cancelorder, name='cancelorder'),
    path('findorder', views.findorder, name='findorder'),
    path('addProduct', views.addProduct, name='addProduct'),
]