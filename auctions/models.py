from django.contrib.auth.models import AbstractUser
from django.db import models

class Category(models.Model):
    name_category = models.CharField(max_length=25)
    def __str__(self):
        return f'{self.id} {self.name_category}'

class AuctionListing(models.Model):
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=64)
    start_bid = models.FloatField()
    image = models.URLField() ##url
    category = models.CharField(max_length=25)
    winner = models.CharField(max_length=26, null=True)
    active = models.BooleanField(null=True)
    owner = models.CharField(max_length=26, null=True)
    
    def __str__(self):
        return f'{self.id}: {self.title} , {self.description} with {self.start_bid}'

class User(AbstractUser):
    listings = models.ManyToManyField(AuctionListing, blank=True, related_name='editors')  ##error a corregir

class Bid(models.Model):
    bid = models.FloatField()
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='belongs')
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctioneers')

    def __str__(self):
        return f'{self.bid} of {self.user} on {self.auction_listing}' 

class Comment(models.Model):
    comment = models.CharField(max_length=64)
    product = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='products')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenters')

    def __str__(self):
        return f'{self.comment} by {self.user}'

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owners')
    own_list = models.ManyToManyField(AuctionListing, blank=True, related_name='watchlists')
    
    def __str__(self):
        return f'{self.own_list} and {self.user}' 