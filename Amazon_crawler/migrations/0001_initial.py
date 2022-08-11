# Generated by Django 3.2 on 2022-08-11 03:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EbayByProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, null=True)),
                ('price', models.CharField(max_length=20, null=True)),
                ('ratings', models.CharField(max_length=20, null=True)),
                ('Condition', models.CharField(max_length=250, null=True)),
                ('Brand', models.CharField(max_length=250, null=True)),
                ('AvailbleQuantity', models.CharField(max_length=250, null=True)),
                ('SoldQuantity', models.CharField(max_length=250, null=True)),
                ('imageUrl', models.CharField(max_length=250, null=True)),
                ('Producturl', models.CharField(max_length=250, null=True)),
                ('TaskId', models.UUIDField()),
                ('Account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='UserAccount', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['title', 'price'],
            },
        ),
        migrations.CreateModel(
            name='AmazonByProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, null=True)),
                ('price', models.CharField(max_length=20, null=True)),
                ('ratings', models.CharField(max_length=250, null=True)),
                ('brand', models.CharField(max_length=250, null=True)),
                ('asin', models.CharField(max_length=250, null=True)),
                ('amazon_choice', models.CharField(max_length=250, null=True)),
                ('Producturl', models.CharField(max_length=700, null=True)),
                ('taskId', models.UUIDField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_account_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['title', 'price'],
            },
        ),
    ]
