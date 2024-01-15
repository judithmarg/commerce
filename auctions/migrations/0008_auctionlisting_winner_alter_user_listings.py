# Generated by Django 4.2.3 on 2024-01-15 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auctionlisting_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='winner',
            field=models.CharField(max_length=26, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='listings',
            field=models.ManyToManyField(blank=True, related_name='editors', to='auctions.auctionlisting'),
        ),
    ]
