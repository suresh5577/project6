import json

from django.contrib import messages
from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import render, redirect
import random

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from adminapp.models import Admin,Merchant,Product


def logincheck(request):
    uname = request.POST.get('username')
    upass = request.POST.get('password')


    adminObj=Admin.objects.get(username=uname,password=upass)
    if adminObj:
        return render(request,'welcome.html',{'data':adminObj})
    else:
        messages.info(request, 'in valid credentials')
        return redirect('/')


def addMerchant(request):
    merchantObj = Merchant.objects.all()
    if merchantObj.exists():
        #print(merchantObj)
        id=merchantObj[::-1][0]
        merchantid=id.merchant_id+1

        return render(request,'addmerchant.html',{'data':merchantObj,'id':merchantid})
    else:
        merchantid=100
        return render(request,'addmerchant.html',{'id':merchantid})
def saveMerchant(request):
    merchantid = request.POST.get('merchantid')
    name = request.POST.get('merchantname')
    emai = request.POST.get('merchantemailid')
    no = request.POST.get('contactno')
    middle_value=str(int(merchantid)+len(name))
    midd = len(middle_value)//2
    pas=emai[0]+str(no)[-1]+middle_value[:midd]+emai[1]+middle_value[midd:]+str(no)[0]+emai[2]


    Merchant(merchant_id=merchantid,merchant_name=name,merchant_email=emai,merchant_contact_no=no,merchant_password=str(pas)).save()
    messages.info(request,'Merchant Added Successfully')
    return redirect('/addmerchant/')


def deleteMerchant(request,merchantid):
    Merchant.objects.filter(merchant_id=merchantid).delete()
    messages.info(request, 'Merchant deleted Successfully')
    return redirect('/addmerchant/')

@method_decorator(csrf_exempt,name='dispatch')
class MerchantLogin(View):
    def post(self,request):
        data = request.body
        d1 =json.loads(data)
        try:
            merchantObj=Merchant.objects.get(merchant_email=d1['username'],merchant_password=d1['password'])
        except:
            js = json.dumps({"message": "Some Error"})
            return HttpResponse(js,content_type='application/json')
        else:
            json_data = serialize("json", [merchantObj],fields=('merchant_id','merchant_name','merchant_email','merchant_contact_no'))
            return HttpResponse(json_data, content_type='application/json')



@method_decorator(csrf_exempt,name='dispatch')
class ViewProduct(View):
    def get(self, request,merchantid):
        #print(merchantid)
        try:
            merchantObj=Merchant.objects.get(merchant_id=merchantid)
            #print(merchantObj)
            productObj = Product.objects.filter(merchant=merchantObj)
            #print(productObj)
            if productObj !=None:
                json_data = serialize("json", productObj)
                #print(json_data)
                return HttpResponse(json_data, content_type="application/json")
            else:
                js = json.dumps({"message": "Some Error"})
                return HttpResponse(js, content_type='application/json')

        except ValueError:
            js = json.dumps({"message": "Some Error"})
            return HttpResponse(js, content_type='application/json')



@method_decorator(csrf_exempt,name='dispatch')
class SaveProduct(View):
    def post(self,request):

        data = request.body
        d2=json.loads(data)
        merchantObj = Merchant.objects.get(merchant_id=d2['merchantid'])
        projectObj = Product.objects.all()
        print(projectObj)
        if projectObj.exists():
            proid = projectObj[::-1][0]
            projectid = proid.prod_id + 1

        else:
            projectid = 1001

        Product(prod_id=projectid,
                prod_name=d2['productname'],
                prod_price=d2['productprice'],
                prod_qty=d2['productqty'],
                merchant_id=int(d2['merchantid'])).save()
        json_data = serialize("json", [merchantObj],
                              fields=('merchant_id', 'merchant_name', 'merchant_email', 'merchant_contact_no'))
        return HttpResponse(json_data,content_type='application/json')
        #{'productid': '1001', 'productname': 'samsung mobile', 'productprice': '12500', 'productqty': '10', 'merchantid': '101'}

    def delete(self,request,productid):
        #print(productid)
        productObj = Product.objects.get(prod_id=productid)
        print(productObj)
        print('--------------------------------------------')
        merchantid=productObj.merchant_id
        print(merchantid)
        merchantObj = Merchant.objects.get(merchant_id=merchantid)
        print(merchantObj)
        print('--------------------')
        productObj.delete()
        json_data = serialize("json", [merchantObj],
                              fields=('merchant_id', 'merchant_name', 'merchant_email', 'merchant_contact_no'))
        return HttpResponse(json_data, content_type='application/json')

    def get(self,request,productid):
        productObj=Product.objects.get(prod_id=productid)
        print(productObj)
        json_data=serialize("json",[productObj])
        return HttpResponse(json_data, content_type='application/json')

    def put(self,request,productid):
        try:
            old_product_data = Product.objects.get(prod_id=productid)
        except Product.DoesNotExist:
            json_mess = json.dumps({'error_message':'Given id is not valid'})
            return HttpResponse(json_mess,content_type='application/json')
        else:
            data = request.body
            d2 = json.loads(data)
            print(type(d2))
            print(d2['productname'])
            old_product_data.prod_name=d2['productname']
            old_product_data.prod_price=d2['productprice']
            old_product_data.prod_qty=d2['productqty']
            old_product_data.save()
            print('...........')
            merchantObj = Merchant.objects.get(merchant_id=old_product_data.merchant_id)
            #print(merchantObj)
            json_data = serialize("json", [merchantObj],
                                  fields=('merchant_id', 'merchant_name', 'merchant_email', 'merchant_contact_no'))
            return HttpResponse(json_data, content_type='application/json')

@method_decorator(csrf_exempt,name='dispatch')
class ChangePassword(View):
    def put(self,request,mail):
        try:
            merchant_mail = Merchant.objects.get(merchant_email=mail)
        except Product.DoesNotExist:
            json_mess = json.dumps({'error_message':'Given Email is not valid'})
            return HttpResponse(json_mess,content_type='application/json')
        else:
            data = request.body
            d3 = json.loads(data)
            if merchant_mail.merchant_password == d3['merchantoldpas']:
                merchant_mail.merchant_password=d3['merchantnewpas']
                merchant_mail.save()
                json_mess = json.dumps({'message': 'Password Changed Successfully'})
                return HttpResponse(json_mess, content_type='application/json')

            else:
                json_mess = json.dumps({'message': 'Password Can not Changed'})
                return HttpResponse(json_mess, content_type='application/json')
