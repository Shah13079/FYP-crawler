from django.contrib import admin

# Register your models here.

from Amazon_crawler import models

class CustomerAdmin(admin.ModelAdmin):
    list_display=['title','price','ratings','Brand','Condition','Producturl']
    ordering=['title','price']
    list_per_page=50

admin.site.register(models.EbayByProduct,CustomerAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display=['title','price','ratings','brand','asin','Producturl']
    ordering=['title','price']
    list_per_page=50

admin.site.register(models.AmazonByProduct,CustomerAdmin)

