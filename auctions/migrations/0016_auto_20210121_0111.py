# Generated by Django 3.1.4 on 2021-01-21 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='highestBid',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
