# Generated by Django 4.2.3 on 2024-01-15 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auctionlisting_winner_alter_user_listings'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='owner',
            field=models.CharField(max_length=26, null=True),
        ),
    ]
