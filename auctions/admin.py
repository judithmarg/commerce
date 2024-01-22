from django.contrib import admin

from .models import AuctionListing, Category, WatchList, Comment, Bid, User


# Register your models here.

#class AuctionListingAdmin(admin.ModelAdmin):
    #list_display = ('id', 'title', 'description', )


class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ('listings', )

admin.site.register(AuctionListing)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(WatchList)
admin.site.register(User, UserAdmin)