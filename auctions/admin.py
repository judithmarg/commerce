from django.contrib import admin

from .models import AuctionListing, Category, WatchList, Comment, Bid


# Register your models here.
admin.site.register(AuctionListing)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(WatchList)
