from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, WatchList, AuctionListing

class NewListing(forms.Form):
    title = forms.CharField(label='Titulo de la pagina')
    descrip = forms.CharField(max_length=120)
    bid = forms.IntegerField()
    image = forms.URLField()
    category = forms.CharField()

class ListingBid(forms.Form):
    bid_current = forms.FloatField()

watchlist = WatchList()

def index(request):
    return render(request, "auctions/index.html",{
        'listings': AuctionListing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    print(AuctionListing.objects.all())
    return render(request, 'auctions/create.html', {
        'listings': AuctionListing.objects.all(),
        'form' : NewListing()
    })

def do_listing(request):
    if request.method == 'POST':
        form = NewListing(request.POST)
        if form.is_valid():
            new_listing = AuctionListing(
                ###pk = count.ver(), la BD las genera automaticamente
                title = form.cleaned_data['title'],
                description = form.cleaned_data['descrip'],
                start_bid = form.cleaned_data['bid'],
                image = form.cleaned_data['image'],
                category = form.cleaned_data['category']
            )
            new_listing.save()
            print(new_listing)
        return render(request, 'auctions/index.html',{
            'listings': AuctionListing.objects.all()
        })
    else:
        return render(request, 'auctions/create.html')
    
def listing(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'editor': listing.listingsmuch.all(),
        'categories' : listing.categories.all(),
        'form_bid': ListingBid()
    })

def bid(request, listing_id):
    if request.method == 'POST':
        item = AuctionListing.objects.get(pk=listing_id)
        editors = User.objects.get(pk=int(request.POST['editor']))
        editors.listings.add(item)
        category = category.objects.get(pk=int(request.POST['category']))
        category.categories.add(item)
        return HttpResponseRedirect(reverse('listing', args=(listing.id,)))

@login_required
def saveWatchlist(request, listing_id):
    if request.method == 'POST':
        itemCurrent = AuctionListing.objects.get(pk=listing_id)
        if itemCurrent in watchlist.objects():
            watchlist.own_list.remove(itemCurrent)
        else: 
            watchlist.own_list.add(itemCurrent) ##watchlists
        print(watchlist)
        return HttpResponseRedirect(reverse('listing', args=(listing.id, )))

