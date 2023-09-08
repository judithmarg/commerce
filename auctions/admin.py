from django.contrib import admin

from .models import AuctionListing, Category, WatchList, Comment, Bid


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    filter_horizontal = ('listingspossible',)

admin.site.register(AuctionListing, CategoryAdmin)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(WatchList)
