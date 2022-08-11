from compat import get_current_site
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.db.models import Q
import csv
from Amazon_crawler.models import EbayByProduct, AmazonByProduct
from django.contrib import auth
from django.contrib import messages


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

from accounts.task import scrape_ebay_by_products,scrape_amazon_products
import uuid


def home(request):
    return render(request,'crawl.html')
            


@login_required
def ebay_By_products(request):
    current_user = auth.get_user(request)
    current_user_id=current_user.id
    current_site=get_current_site(request)

    if request.method=="POST":
        products_urls=request.POST.get('EBP')
        taskid=uuid.uuid4()

        if 'ebay' not in products_urls or "pgn=" in products_urls:
            messages.warning(request,f"""Please Paste valid URLS of ebey Products !"""    )
            return render(request,'Ebay_by_products.html',{"UrlError":True})

        elif 'ebay' in products_urls:
            products_urls=products_urls.split()
            scrape_ebay_by_products.delay(products_urls,current_user_id,taskid,str(current_site))
            messages.success(request,f"""Your task : [{taskid}] has been added successfully, You will be notified as soon through email as job get finished !"""    )
            return render(request,'Ebay_by_products.html',{"Entities":"Entities"})
    return render(request,'Ebay_by_products.html')



@login_required
def amazon_by_pro(request):
    current_user = auth.get_user(request)
    current_user_id=current_user.id
    current_site=get_current_site(request)

    if request.method=="POST":
        products_urls=request.POST.get('ABP')
        taskid=uuid.uuid4()

        if 'amazon' not in products_urls:
            messages.warning(request,f"""Please Paste valid URLS of ebey Products !"""    )
            return render(request,'amazon_by_products.html',{"UrlError":True})

        if 'amazon' in products_urls:
            print("this is url",products_urls)
            
            products_urls=products_urls.split()

            messages.success(request,f"""Your task : [{taskid}] has been added successfully, You will be notified as soon through email as job get finished !"""    )
            
            scrape_amazon_products.delay(products_urls,current_user_id,taskid,str(current_site))
    return render(request,'amazon_by_products.html',{"UrlError":True})
 



@login_required
def download_data(request,task_id):
    if request.user.is_authenticated ==True:
        current_user = auth.get_user(request)
        current_user=current_user.id

        response=HttpResponse(content_type='text/csv')
        writer=csv.writer(response)
        writer.writerow(["title","price",'ratings',"shipping","Condition","Brand","AvailbleQuantity","SoldQuantity","imageUrl","Producturl"])
        
        query_set=EbayByProduct.objects.filter(Q(Account_id=int(current_user)) & Q(TaskId=task_id)).values_list(
            "title","price",'ratings',"Condition","Brand","AvailbleQuantity","SoldQuantity","imageUrl","Producturl",)

        for each in query_set:
            writer.writerow(each)

        response['Content-Disposition']='attachment; filename="Ebay-scraped.csv"'
        return response
    else:
        redirect ('login')

    

@login_required
def download_amazon(request,task_id):
    if request.user.is_authenticated ==True:
        current_user = auth.get_user(request)
        current_user=current_user.id

        response=HttpResponse(content_type='text/csv')
        writer=csv.writer(response)
        writer.writerow(["title","price","ratings","brand","asin","amazon_choice","Producturl"])
        
        query_set=AmazonByProduct.objects.filter(Q(account_id=int(current_user)) & Q(taskId=task_id)).values_list(
            "title","price","ratings","brand","asin","amazon_choice","Producturl")

        for each in query_set:
            writer.writerow(each)

        response['Content-Disposition']='attachment; filename="amazon-data-scraped.csv"'
        return response
    else:
        redirect ('login')
