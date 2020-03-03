import json

import requests
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .utils import localhost


# Create your views here.
def showIndex(request):
    return render(request,'index.html')

def loginCheck(request):
    username = request.POST.get('username')
    pas = request.POST.get('password')
    d1={'username':username,'password':pas}
    json_data = json.dumps(d1)
    try:
        res = requests.post(localhost+"/merchantlogin/", data=json_data)
        print(res.status_code)
        data = res.json()[0]
        print(data)

    except requests.exceptions.ConnectionError:
        print("Sever is not Available")
    except KeyError:
        return render(request,'index.html',{'message':'invalid Credentials'})

    else:
        return render(request,'home.html',{'data':data})


def viewproduct(request):
    merchantid=request.GET.get('idno')
    try:
        res = requests.get(localhost+"/viewproduct/"+str(merchantid)+'/')
        if res.json()!=[]:
            pk = merchantid
            print(res.status_code)
            pro=res.json()
            print(pro)
            return render(request,'addproduct.html',{'prodata':pro,'data':pk})
        else:
            pk = merchantid
            return render(request, 'addproduct.html', {'message':'please add products','data':pk})
    except ValueError:
        print('error')
            #messages.info(request,'No data available please add product')
            #return redirect('')


def saveProduct(request):
    prod_name = request.POST.get('prodname')
    prod_price = request.POST.get('prodprice')
    prod_qty = request.POST.get('prodqty')
    merchant_id = request.POST.get('merchantid')
    d2={'productname':prod_name,'productprice':prod_price,'productqty':prod_qty,'merchantid':merchant_id}
    json_data = json.dumps(d2)
    res = requests.post(localhost+"/saveproduct/", data=json_data)
    print(res.status_code)
    data = res.json()[0]
    print(data)
    return render(request,'home.html',{'data':data})


def delectProduct(request,proid):
    print(proid)
    res = requests.delete(localhost+"/deleteproduct/"+str(proid)+"/")
    print(res.status_code)
    data=res.json()[0]
    return render(request, 'home.html', {'data': data})


def updateProduct(request):
    prod_id = request.POST.get('prodno')
    prod_name = request.POST.get('prodname')
    prod_price = request.POST.get('prodprice')
    prod_qty = request.POST.get('prodqty')
    merchant_id = request.POST.get('merchantid')
    d2 = {'productname': prod_name, 'productprice': prod_price, 'productqty': prod_qty, 'merchantid': merchant_id}
    json_data = json.dumps(d2)
    res = requests.put(localhost+"/updateproduct/"+prod_id+"/",data=json_data)
    print(res.status_code)
    data = res.json()[0]
    print(data)
    return render(request, 'home.html', {'data': data})


def showUpdate(request,proid):
    res = requests.get(localhost+"/showproduct/" + str(proid) + '/')
    print(res.status_code)
    data=res.json()[0]

    return render(request,'update.html',{'data':data})


def chengePassword(request):
    return render(request,'passwordchange.html')


def checkCheangePas(request):
    merchantmail = request.POST.get('email')
    merchantoldpas = request.POST.get('oldp')
    merchantnewpas1 = request.POST.get('new1')
    merchantnewpas2 = request.POST.get('new2')
    if merchantnewpas1 == merchantnewpas2:
        d3={
            'merchantoldpas':merchantoldpas,
            'merchantnewpas':merchantnewpas1
        }
        js=json.dumps(d3)
        res = requests.put(localhost+"/updatpassword/"+merchantmail+"/", data=js)
        print(res.status_code)
        print(res.json())
        return render(request,'index.html',{'message':'password Changed Successfully please log in'})
    else:
        return render(request,'index.html',{'message':'Password not matching'})