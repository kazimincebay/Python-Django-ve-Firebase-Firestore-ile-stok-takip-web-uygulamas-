from django.shortcuts import render,redirect
from requests.sessions import session
from django.contrib import auth,messages
import uuid
import firebase_admin
from firebase_admin import credentials,firestore


cred=credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

import pyrebase

config = {
  #firebase config bilgileri
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firestore.client()
storage = firebase.storage() 



def signIn(request):   
    return render(request,"signin.html")


    
def postsign(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = authe.sign_in_with_email_and_password(email, password)
    except:
        message="E-Mail Adresi veya Şifre Yanlış"
        return render(request,"signin.html",{"msg":message})
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return redirect('checkproduce')

def updatestock(request):
    productuid=request.POST.get('productuid')

    idtoken = request.session['uid']
    a=authe.get_account_info(idtoken)

    context={
        'productuid':productuid,
    }

    return render(request,"updatestock.html",context)

def updatestockk(request):
    productuid=request.POST.get('productuid')
    producestock=request.POST.get('producestock')

    idtoken = request.session['uid']
    a=authe.get_account_info(idtoken)

    database.collection("Products").document(productuid).update({"produceStock":producestock})
    
    return redirect("checkproduce")
def addproduce(request):
    idtoken = request.session['uid']
    a=authe.get_account_info(idtoken)
    return render(request, "addproduce.html")

def addProduce(request):
   idtoken = request.session['uid']
   a=authe.get_account_info(idtoken)
   produceCode=str(uuid.uuid1())
   produceImageURL=request.POST.get('produceImageURL')
   produceCategory=request.POST.get('produceCategory')
   produceName=request.POST.get('produceName')
   produceStock=request.POST.get('produceStock')
   producePrice=request.POST.get('producePrice')
   produceDescription=request.POST.get('produceDescription')

   
   idtoken = request.session['uid']
   a=authe.get_account_info(idtoken)
   
    
   data = {
            "produceImageURL":produceImageURL,
            "produceCategory":produceCategory,
            "produceCode":produceCode,
            "produceName":produceName,
            "produceStock":produceStock,
            "producePrice":producePrice,
            "produceDescription":produceDescription
            
            

        }

   database.collection("Products").add(data)

   return redirect("checkproduce")
   
def addcustomer(request):
    idtoken = request.session['uid']
    a=authe.get_account_info(idtoken)
    return render(request,"addcustomer.html")

def addCustomer(request):
   idtoken = request.session['uid']
   a=authe.get_account_info(idtoken)
   customerId=str(uuid.uuid1())
   customerName=request.POST.get('customerName')
   customerSurname=request.POST.get('customerSurname')
   customerMail=request.POST.get('customerEmail')
   customerVergiNo=request.POST.get('customerVergiNo')
   customerPhoneNumber=request.POST.get('customerPhoneNumber')
   customerAdress=request.POST.get('customerAdress')
   

   
   idtoken = request.session['uid']
   a=authe.get_account_info(idtoken)
   
    
   data = {
            "customerId":customerId,
            "customerName":customerName,
            "customerSurname":customerSurname,
            "customerMail":customerMail,
            "customerVergiNo":customerVergiNo,
            "customerPhoneNumber":customerPhoneNumber,
            "customerAdress":customerAdress
            
            
            

        }

   database.collection("Customers").add(data)

   return redirect("customers")

def showcustomer(request):
    idtoken = request.session['uid']
    a=authe.get_account_info(idtoken)
    customerlist = []
    customers=database.collection("Customers").get()

    
    for customer in customers:
        data = customer.to_dict()
        customerlist.append(data)
    

    context = {
       'customerlist':customerlist,

    }   
    return render(request,"checkcustomer.html",context)

def selectcustomer(request):
    idtoken = request.session['uid']
    a=authe.get_account_info(idtoken)
    customerlist=[]
    customers=database.collection("Customers").get()

    for customer in customers:
        data = customer.to_dict()
        customerlist.append(data)

    context = {
       'customerlist':customerlist,
       
       

    }   
    return render(request,"selectcustomer.html",context)

def confirmorder(request):
    idtoken = request.session['uid']
    a=authe.get_account_info(idtoken)

    productlist=[]
    numberlist=[]
    customer=customerlist[0]
    productlist=orderproductslist
    numberlist=orderproductsnumberlist
    products=[]
    productprc=[]
    ttlprc=[]
    productuid=[]
    productstk=[]
    totalprice=0
    
    

    
    
    for j in productlist:
        produces=database.collection("Products").where("produceCode","==",j).get()

        for i in produces:
            data=i.to_dict()
            id=i.id
            data["id"]=id
            products.append(data["produceCode"])
            productprc.append(int(data["producePrice"]))
            productuid.append(data["id"])
            productstk.append(int(data["produceStock"]))
    
    for b in range(0,len(productprc)):
        ttlprc.append((productprc[b])*(numberlist[b]))
    
    
    for sayi in ttlprc:
        totalprice+=sayi
     
    
    
    from datetime import datetime
    an=datetime.now()
    billId=str(uuid.uuid1())
    billdateyear=str(an.year)
    billdatemonth=str(an.month)
    billdateday=str(an.day)
    billdate=billdatemonth+"/"+billdateyear
    billcreatedate=billdateday+"/"+billdatemonth+"/"+billdateyear
    
    
    
    taxprice=((totalprice*18)/100)
    taxtotalprice=((totalprice*18)/100)+totalprice
    for i in range(0,len(numberlist)):
        if(productstk[i]>0):
            silstok=productstk[i]-numberlist[i]
            database.collection("Products").document(productuid[i]).update({"produceStock":(int(silstok))})
        if(productstk[i]<=0):
            message=productuid[i]+" Ürününde Stok Yok"
            return render(request,"checkproduce.html",{"msg":message})

    context={
        'billId':billId,
        'billcreatedate':billcreatedate,
        'billdate':billdate,
        'customer':customer,
        'products':products,
        'numberlist':numberlist,
        'totalprice':totalprice,
        'taxprice':taxprice,
        'taxtotalprice':taxtotalprice,
        
    }

    database.collection("Bills").add(context)
    



    orderproductslist.clear()
    orderproductsnumberlist.clear()
    totalprice=0
    taxprice=0
    
    
    
    return redirect("checkbills")

customerlist=[]
orderproductslist=[]
orderproductsnumberlist=[]



def selectproduce(request):
    idtoken = request.session['uid']
    a=authe.get_account_info(idtoken)
    productlist=[]
    produces=database.collection("Products").get()

    for produce in produces:
        data = produce.to_dict()
        productlist.append(data)
    
    customer=request.POST.get('customerId')
    customerlist.append(customer)
    

    context = {
       'productlist':productlist,
       'orderproductslist':orderproductslist,
       'orderproductsnumberlist':orderproductsnumberlist,

    }  


    
    
    

    
    return render(request,"selectproduce.html",context)





def addproducelist(request):
    adet=request.POST.get('adet')
    produceinfo=request.POST.get('produceinfo')
    orderproductslist.append(produceinfo)
    orderproductsnumberlist.append(int(adet))
    
    
    
    return redirect("selectproduce")

def clearorderproductlist(request):
    orderproductslist.clear()
    orderproductsnumberlist.clear()
    

    return redirect('selectproduce')


def checkbills(request):
    idtoken = request.session['uid']
    a=authe.get_account_info(idtoken)
    billliste=[]
    cstlist=[]
    bills=database.collection("Bills").get()
    customer=database.collection("Customers").get()

    for bill in bills:
        data = bill.to_dict()
        billliste.append(data)
        


    
    for cst in customer:
        data = cst.to_dict()
        cstlist.append(data)
    

    context = {
       'billliste':billliste,
       'cstlist':cstlist,
    }  
    return render(request,"checkbills.html",context)

def checkspecialbill(request):
    billdate=request.POST.get("billdate")
    cstıd=request.POST.get("cstıd")
    bills=database.collection("Bills").where("billdate","==",billdate).where("customer","==",cstıd).get()
    numberlist=orderproductsnumberlist
    productlist=orderproductslist
    billlist=[]
    
    
    for bill in bills:
        data = bill.to_dict()
        billlist.append(data)
    
    context={
        'billlist':billlist,
        'numberlist':numberlist,
        'productlist':productlist,
    }
    return render(request,"checkspecialbill.html",context)

def checkproduce(request):
    idtoken = request.session['uid']
    a=authe.get_account_info(idtoken)
    productlist=[]
    produces=database.collection("Products").get()
     
    for produce in produces:
        data = produce.to_dict()
        id=produce.id
        data["id"]=id
        productlist.append(data)
    
    context = {
       'productlist':productlist,

    }  
    return render(request,"checkproduce.html",context)

def logout(request):
    try:    
        del request.session['uid']
    except:
        pass
    return render(request,"signin.html")


