from django.shortcuts import render
from django.http import JsonResponse
from pymongo import MongoClient
from bson import json_util
from email.message import EmailMessage
from datetime import date
import smtplib
import json
from django.views.decorators.csrf import csrf_exempt

client = MongoClient('mongodb+srv://ashwath:qwertyashwath@main.ezawg.gcp.mongodb.net/SrinivasaSiddhaStores?retryWrites=true&w=majority')
db = client.get_database('SrinivasaSiddhaStores')

@csrf_exempt
def changeImage(request):
    records = db.products
    data = json.loads(request.body)
    id = data['id']
    url = data['url']
    print(id)
    records.update_one({'id':id}, {'$set':{'image_url': url}})
    res = records.find_one({'id':id})
    return JsonResponse(json.loads(json_util.dumps(res)), safe=False)

def getCurrOrders(request):
    records = db.orders
    res = list(records.find({'completed': 0}))
    return JsonResponse(json.loads(json_util.dumps(res)), safe=False)

def getOldOrders(request):
    records = db.orders
    res = list(records.find({'completed': 1}))
    return JsonResponse(json.loads(json_util.dumps(res)), safe=False)

def getDelOrders(request):
    records = db.orders
    res = list(records.find({'completed': 2}))
    return JsonResponse(json.loads(json_util.dumps(res)), safe=False)

@csrf_exempt
def delivery(request):
    data = json.loads(request.body)
    refno = data['refno']
    courier = data['courier']
    id = data['id']

    records = db.orders
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    
    records.update_one({'id':int(id)}, {'$set':{
        'delivery_details': {
            'refno': refno,
            'courier': courier,
            'dispatch_date': d1
        },
        'completed': 1
        }})

    res = records.find_one({'id':int(id)})

    name = res['name']
    email = res['email']

    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login('srinivasasiddhastores@gmail.com', 'nstxxexzlwzvizsx')

    msg = EmailMessage()
    msg.set_content(f'Hello {name}!,\n\n Your order has been dispatched from our side. We have sent through {courier}. And the reference number for tracking your order is: {refno}.\n\nThankyou! Keep connected with us!')

    msg['Subject'] = 'Order Dispatched!'
    msg['From'] = 'srinivasasiddhastores@gmail.com'
    msg['To'] = email

    s.send_message(msg)
    s.quit()

    return JsonResponse({'res':'mail sent'}, safe=False)

@csrf_exempt
def cancelorder(request):
    data = json.loads(request.body)
    id = data['id']

    records = db.orders
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    
    records.update_one({'id':int(id)}, {'$set':{
        'delivery_details': {
            'refno': 'cancelled',
            'courier': 'cancelled',
            'dispatch_date': d1
        },
        'completed': 2
        }})

    res = records.find_one({'id':int(id)})

    name = res['name']
    email = res['email']

    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login('srinivasasiddhastores@gmail.com', 'nstxxexzlwzvizsx')

    msg = EmailMessage()
    msg.set_content(f'Hello {name}!,\n\n Sorry to inform you that, there was a technical issue on the order that you have placed. So we have gone for a refund to manage this. Hopefully, you will get your refunded amount by 5-7 working days.\n\nThankyou! Keep connected with us!')

    msg['Subject'] = 'Order Cancelled!'
    msg['From'] = 'srinivasasiddhastores@gmail.com'
    msg['To'] = email

    s.send_message(msg)
    s.quit()


    return JsonResponse(json.loads(json_util.dumps(res)), safe=False)

@csrf_exempt
def findorder(request):
    data = json.loads(request.body)
    id = data['id']
    records = db.orders
    res = records.find_one({'id':int(id)})
    return JsonResponse(json.loads(json_util.dumps(res)), safe=False)

@csrf_exempt
def addProduct(request):
    records = db.products
    data = json.loads(request.body)

    new_product = {
    'id' : 'new_product',
    'product_name' : data['product_name'],
    'company' : data['company'],
    'category' : data['category'],
    'price' : data['price'],
    'description' : data['description'],
    'image_url' : data['image_url'],
    'available' : data['available']
    }
    records.insert_one(new_product)
    new_id = str(new_product['_id'])
    records.update_one({'id':'new_product'}, {'$set':{'id': new_id}})
    return JsonResponse(json.loads(json_util.dumps(new_product)), safe=False)