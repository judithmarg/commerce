from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=64)
    start_bid = models.FloatField()

    def __str__(self):
        return f'{self.id}: {self.title} , {self.description}'
    
class Bid(models.Model):
    

class Comment():