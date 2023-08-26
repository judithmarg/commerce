from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=64)
    start_bid = models.FloatField()
    image = models.ImageField() ##url
    category = models.CharField(max_lenght=25)

    def __str__(self):
        return f'{self.id}: {self.title} , {self.description} with {self.start_bid}'
    
class Bid(models.Model):
    bid = models.FloatField()
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='belongs')
    user_made = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctioneers')

    def __str__(self):
        return f'{self.bid} of {self.user_made} on {self.auction_listing}' 

class Comment(models.):