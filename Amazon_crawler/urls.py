from django.urls import path
from . import views

app_name = "Amazon_crawler"

# URLConf
urlpatterns = [
    path('', views.home,name=''),
    path('best-selling/',views.home,name='best-selling'),
    path('download/<task_id>/',views.download_data,name='download_data'),
    path('download_amazon/<task_id>/',views.download_amazon,name='download_amazon'),

 
    path("EBP/",views.ebay_By_products,name='EBP'),
    path("ABP/",views.amazon_by_pro,name='ABP')

            ]


