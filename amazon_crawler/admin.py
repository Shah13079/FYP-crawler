from django.contrib import admin
from amazon_crawler import models

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display=['title','price','rating','brand','condition','product_url']
    ordering=['title','price']
    list_per_page=50
admin.site.register(models.EbayByProduct,CustomerAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display=['title','price','rating','brand','asin','product_url']
    ordering=['title','price']
    list_per_page=50
admin.site.register(models.AmazonByProduct,CustomerAdmin)

