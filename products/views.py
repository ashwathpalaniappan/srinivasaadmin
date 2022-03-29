from pickle import NONE, TRUE
from tkinter import FALSE
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import razorpay
client = razorpay.Client(auth=("rzp_test_6YBqanCDHfp17o", "PO5u5iHXTSk8TfvupciZvvIs"))

# context = {
#     'products': [],
#     'cart_number': 0,
#     'cart_items': [{},{}],
#     'delivery': 50,
#     'sub_total': 50
# }
# def session_handler(request):
    
# request.session('context')

def home(request):
    return render(request,'products/shopAdmin.html')

def thankyou(request):
    if 'context' in request.session:
        del request.session['context']
        if 'order' in request.session:
            del request.session['order']
    
    return render(request,'products/thankyou.html')

def oldorders(request):
    res = requests.get('http://localhost:7000/backend/getOldOrders')
    orders = res.json()
    request.session['old_orders'] = orders
    data = {}
    data['orders'] = orders    
    return render(request,'products/currorders.html', data)

def currorders(request):
    res = requests.get('http://localhost:7000/backend/getCurrOrders')
    orders = res.json()
    request.session['curr_orders'] = orders
    data = {}
    data['orders'] = orders    
    return render(request,'products/currorders.html', data)

def delorders(request):
    res = requests.get('http://localhost:7000/backend/getDelOrders')
    orders = res.json()
    request.session['del_orders'] = orders
    data = {}
    data['orders'] = orders    
    return render(request,'products/currorders.html', data)

def order(request,orderid):

    if request.method == 'POST':
        json_data = {
        'refno': request.POST['refno'],
        'courier': request.POST['courier'],
        'id': orderid
        }
        api_url = 'http://localhost:7000/backend/delivery'
        r = requests.post(url=api_url, json=json_data)     

        return redirect('/oldorders')

    api_url1 = 'http://localhost:7000/backend/findorder'
    resp = requests.post(url=api_url1, json={'id': orderid})
    order_item = resp.json()
    
    return render(request,'products/order.html', order_item)

def cancelorder(request,orderid):
    json_data = {
    'id': orderid
    }
    api_url = 'http://localhost:7000/backend/cancelorder'
    res = requests.post(url=api_url, json=json_data)
    order = res.json()
    payment_id = order['payment']['payment_id']
    resp = client.payment.refund(payment_id)
    print(resp)
    return redirect('/delorders')

def changeimg(request):
    if request.method == 'POST':
        json_data = {
        'id': request.POST['id'],
        'url': request.POST['url'],
        }
        api_url = 'http://localhost:7000/backend/changeImage'
        r = requests.post(url=api_url, json=json_data)
        return redirect('/')

    return render(request,'products/changeimage.html')