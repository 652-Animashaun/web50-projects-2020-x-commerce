# Generated by Django 3.1.4 on 2021-01-07 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_listing_vendor'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='currBid',
            field=models.IntegerField(default=1),
        ),
    ]
