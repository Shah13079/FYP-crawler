from django.db import models
from accounts.models import Account

class EbayByProduct(models.Model):
    title=models.CharField(max_length=300,null=True)
    price=models.CharField(max_length=20,null=True)
    ratings=models.CharField(max_length=20,null=True)
    Condition=models.CharField(max_length=250,null=True)
    Brand=models.CharField(max_length=250,null=True)
    AvailbleQuantity=models.CharField(max_length=250,null=True)
    SoldQuantity=models.CharField(max_length=250,null=True)
    imageUrl=models.CharField(max_length=250,null=True)
    Producturl=models.CharField(max_length=250,null=True)
    TaskId=models.UUIDField(null=False)
    Account=models.ForeignKey(Account,on_delete=models.CASCADE,related_name='UserAccount',null=False)
    
    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering=['title', 'price']


class AmazonByProduct(models.Model):
    title=models.CharField(max_length=300,null=True)
    price=models.CharField(max_length=20,null=True)
    ratings=models.CharField(max_length=250,null=True)
    brand=models.CharField(max_length=250,null=True)
    asin=models.CharField(max_length=250,null=True)
    amazon_choice=models.CharField(max_length=250,null=True)
    Producturl=models.CharField(max_length=700,null=True)
    taskId=models.UUIDField(null=False)
    account=models.ForeignKey(Account,on_delete=models.CASCADE,related_name='user_account_id',null=False)
    

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering=['title', 'price']
