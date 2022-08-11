import requests
from scrapy.selector import Selector
from Amazon_crawler.models import EbayByProduct,AmazonByProduct
from Amazon_crawler.views import headers
from .models import Account
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import numpy
import re
from concurrent.futures import ThreadPoolExecutor
import urllib3
from os import getcwd,path
import logging
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}
    

#Sending email on conformation
def sending_task_confirmation_mail(user_id,mail_subject_is,task_id,current_site,SPages,total_products,section):


    if total_products != None and SPages==None:
        pages_nd_products='Products'
        total=total_products

    elif SPages!=None and total_products is None:
        pages_nd_products='Pages'
        total=SPages


    user=Account.objects.get(pk=user_id)
    mail_subject=mail_subject_is
    task_id=task_id.replace("-",'')

    if section=="AP":
        download_link=f'http://{current_site}/crawlers/download_amazon/{task_id}'
    else:
        download_link=f'http://{current_site}/crawlers/download/{task_id}'
    

    message=render_to_string(
        'accounts/job_status.html',
        {
            'download_link':download_link,
            'couvnt':total,
            "task_id":task_id,
            'user':user,
            'type':pages_nd_products
                }

                )

    to_email=user.email
    send_email=EmailMessage(mail_subject,message,to=[to_email])
    send_email.send()


#Scrape Ebay products  by Urls
def f_scrape_ebay_by_products(products_urls,current_user,task_id,current_site):
    headers = {"X-Crawlera-Region" : "US",

                'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
               
                }
    
    proxy_host = "proxy.zyte.com"
    proxy_port = "8011"
    proxy_auth = "6e5fa123c7e74c04871a2661ffb87ab8:" # Make sure to include ':' at the end
    proxies = {"https": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
        "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}



    Logs={}
    total_products_scraped=0
    for each in products_urls:
        try:
            responser=requests.get(each,proxies=proxies,
                            verify=path.join(path.join(getcwd(),"accounts"),"zyte-proxy-ca.crt") ,)

            print("status is:",responser.status_code)
            if 'Looks like this page is missing. If you still need help' in responser.text:
                pass
            else:
                response_selector=Selector(text=responser.text)
                
                title=response_selector.xpath("//h1[@itemprop='name']/text()").get()
                title_sec=response_selector.xpath("//h1[@class='product-title']/text()").get()
                if not title and title_sec:
                    title=title_sec

                if title is None:
                    title=response_selector.xpath("//h1/span/text()").get()

                ratings=response_selector.xpath('//span[@class="review--start--rating"]/text()').get()
                
                price=response_selector.xpath("//div[contains(text(),'Price:')]/following-sibling::div//span/text()").get()
                if price is None or 'Discounted' in price :
                    price=response_selector.xpath("//div[contains(text(),'Price:')]/following-sibling::div//span[position() = last()]/text()").get()
                if price is None:
                    price=response_selector.xpath('//div[@class="display-price"]/text()').get()
                if price:price=price.strip()
                

                brand=response_selector.xpath("//span[@itemprop='brand']//span/text()").get()
                if not brand:
                    brand=response_selector.xpath('//div[contains(text(),"Brand")]/following-sibling::node()/text()').get()

                Condition=response_selector.xpath("//div[contains(text(),'Condition')]/following-sibling::div/text()").get()
                if Condition is None:Condition=response_selector.xpath("//div/span[contains(text(),'Condition')]/parent::node()/following-sibling::div//span[@class='clipped']/text()").get()

                    

                avail_quanitity=response_selector.xpath("//span[@id='qtySubTxt']/span/text()").get()
                if avail_quanitity:
                    avail_quanitity=avail_quanitity.strip()
                
                sold_quantity=response_selector.xpath("//a[@class='vi-txt-underline']/text()").get()
                
                img_url=response_selector.xpath("//button/div/img[@itemprop='image']/@src").get()
                if img_url is None:img_url=response_selector.xpath("//div[@class='product-image']/img/@src").get()

            

                ERecords  =EbayByProduct()
                ERecords.title=title
                ERecords.price=price
                ERecords.ratings=ratings
                ERecords.Brand=brand
                ERecords.Condition=Condition
                ERecords.AvailbleQuantity=avail_quanitity
                ERecords.SoldQuantity=sold_quantity
                ERecords.imageUrl=img_url
                ERecords.Producturl=each
                ERecords.Account=Account.objects.get(id=current_user)
                ERecords.TaskId=task_id

                ERecords.save()

                total_products_scraped+=1

        except Exception as e:

            mail_subject="System maintainace alert !"

            message=f"To Technical team:\n\n\n\
                Tool Name: [Ebay by Direct Urls]\n\n\
                file Name: engine_function.py\n\
                source link:{each}\n \
                Please Look at the following error in \method name[f_scrape_ebay_by_products]\n\
                \nError:\t\t{e}"

            to_email="Shahhussainofficial@gmail.com"
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()


    Logs['total_products_scraped']=total_products_scraped
    return Logs






#OOP IS USED FOR AMAZON CRAWLER WITH INHERITENCE
#------------------------------------------------------------


class  AmazonProduct:

    logs_dic={'total_scraped_products':0}

    headers = {"X-Crawlera-Region" : "US",

                'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
               
                }
    
    proxy_host = "proxy.zyte.com"
    proxy_port = "8011"
    proxy_auth = "6e5fa123c7e74c04871a2661ffb87ab8:" # Make sure to include ':' at the end
    proxies = {"https": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
        "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}


    def is_amazon_choice(self,values):
        if values:
            if len(values) > 0 :
                return True
            else:
                return numpy.nan


    def remove_extra_string(self,value):
        if value:
            if "out of" in value:
                return value.replace("out of 5 stars","")
    

    def get_curr(self,price):
        if price:
            pattern =  r'(\D*)[\d\,\.]+(\D*)'
            g = re.match(pattern, price.strip()).groups()
            return (g[0] or g[1]).strip()
        else: return None


    def remove_curr(self,price):
        if price:
            pattern =  r'(\D*)[\d\,\.]+(\D*)'
            g = re.match(pattern, price.strip()).groups()
            Currency=(g[0] or g[1]).strip()
            return price.replace(Currency,'').strip()


    #Getting ASIN from Product Url using re
    def get_asin(self,href):
        asin = re.search(r'/[dg]p/([^/?]+)', href, flags=re.IGNORECASE)
        if asin:
            return asin.group(1)


    def sending_requests(self,url,current_user,task_id,current_site):

        html = requests.get(
                            url,
                            proxies=self.proxies,
                            verify=path.join(path.join(getcwd(),"accounts"),"zyte-proxy-ca.crt") ,
                        )
        print("this is response from request:",html.status_code)
        if html.status_code ==503:
            self.sending_requests(self,url,current_user,task_id,current_site)

        elif html.status_code ==200:
            response=Selector(text=html.text)
            self.parse_data(response,current_user,task_id,current_site,str(url))
    


    def threading(self,urls,current_user,task_id,current_site):
        with ThreadPoolExecutor(max_workers=15) as executor:
            for url in urls:
                executor.submit(self.sending_requests,url,current_user,task_id,url) 

    
    
  
    def parse_data(self, response,current_user,task_id,current_site,current_url):

        title=response.xpath("//h1[@id='title']/span/text()").get()
        brand=response.xpath("(//td/span[contains(text(),'Brand')]/following::td)[1]/span/text()").get()

        main_price=self.remove_curr(response.xpath('(//span[@class="a-price-whole"])[1]/text()').get())
        frac_price=self.remove_curr(response.xpath('//span[@class="a-price-fraction"]/text()').get())

        if main_price and frac_price:
            price = main_price+'.'+frac_price

        if main_price and frac_price is None:
            price  = main_price
        
        if not main_price and not frac_price:
            price = ''
        
        
     

        ratings=self.remove_extra_string(response.xpath('(//span[contains(text(),"out of 5 stars")])[1]/text()').get())
        asin=self.get_asin(current_url)
        amazon_choice=response.xpath("//span[contains(text(),'Choice')]/text()").get()
        if amazon_choice is not None:
            amazon_choice=True
        else:
            amazon_choice=numpy.nan
        
        try:
            amazon_records=AmazonByProduct()
            amazon_records.title=title
            amazon_records.price=price
            amazon_records.brand=brand
            amazon_records.ratings=ratings
            amazon_records.asin=asin
            amazon_records.Producturl=current_url
            amazon_records.amazon_choice=amazon_choice
            amazon_records.taskId=task_id
            amazon_records.account=Account.objects.get(id=current_user)
            amazon_records.save()

            self.logs_dic['total_scraped_products']+=1

        except Exception as e:
            mail_subject="System maintainace alert !"

            message=f"To Technical team:\n\n\n\
                Tool Name: [Amazon Data]\n\n\
                file Name: engine_function.py\n\
                source link:{current_url}\n \
                Please Look at the following error in \nmethod name[amazon: parse_data]\n\
                \nError:\t\t{e}"

            to_email="Shahhussainofficial@gmail.com"
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
        
        
    def logs_mail(self, current_user,task_id,current_site):
        if self.logs_dic['total_scraped_products'] >=1:
            subject=f"amazon by products job status - ParseJet"
            sending_task_confirmation_mail(current_user,subject,task_id,current_site,None,self.logs_dic['total_scraped_products'],"AP")


def amazon_product_calling(products_urls,current_user,task_id,current_site):
    print("Product url received in amazon class object:",products_urls)
    object1=AmazonProduct()
    object1.threading(products_urls,current_user,task_id,current_site)
    object1.logs_mail(current_user,task_id,current_site)
   



