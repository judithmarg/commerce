# Generated by Django 4.2.3 on 2023-08-30 22:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlisting_category_watchlist_comment_bid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='list_category',
        ),
    ]
