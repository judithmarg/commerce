from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, WatchList, Comment, AuctionListing, Category , Bid

class NewListing(forms.Form):
    title = forms.CharField(label='Titulo de la pagina')
    descrip = forms.CharField(max_length=120)
    bid = forms.FloatField()
    image = forms.URLField()
    category = forms.CharField()

class ListingBid(forms.Form):
    bid_current = forms.FloatField()

class CommentListing(forms.Form):
    comment_current = forms.CharField()

#watchlist = WatchList()

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
                category = form.cleaned_data['category'],
                active = True,
                owner = request.user.username
            )
            new_listing.save()
        return render(request, 'auctions/index.html',{
            'listings': AuctionListing.objects.all(),
            'last_bid': new_listing.start_bid
        })
    else:
        return render(request, 'auctions/create.html')

@login_required
def listing(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    bids = Bid.objects.filter(auction_listing=listing_id)
    comentarios = Comment.objects.filter(user= request.user, product=listing_id)

    last_bid = bids.order_by('-bid').first()
    if last_bid:
        last_bid_value = last_bid.bid
    else:
        last_bid_value = listing.start_bid

    watchlist = WatchList.objects.filter(user=request.user, own_list=listing)
    in_watchlist = bool(watchlist)
    
    commentsAll = [(com.user.username, com.comment) for com in comentarios]
    print(commentsAll)
    if request.user.username == listing.winner:
        return render(request, 'auctions/win.html')
    else:
        return render(request, 'auctions/listing.html', {
            'listing': listing,
            'editor': listing.winner,  #se coloca el alias dado
            'autor': listing.owner,
            'categories' : listing.categories.all(),
            'last_bid': last_bid_value, #bid = Bid.objects.get(pk=listing_id).get()
            'form_bid': ListingBid(),
            'is_active': listing.active,
            'in_watchlist' : in_watchlist,
            'form_comment': CommentListing(),
            'commentsAll':commentsAll
        })

@login_required
def bid(request, listing_id):
    if request.method == 'POST':
        item = AuctionListing.objects.get(pk=listing_id)
        #editors = User.objects.get(pk=int(request.POST['editor']))
        #editors.listings.add(item)
        #category = Category.objects.get(pk=int(request.POST['category']))
        #category.categories.add(item)

        '''falta mejorar '''
        #bid_current, created = Bid.objects.get_or_create(user=request.user)
        bid_made = float(request.POST['bid_current'])
        bid_created = Bid(bid_made, item.id, request.user)

        if bid_made > item.start_bid: #and bid_made > bid_current.bid: #existe
            bid_created.user = request.user
            bid_created.auction_listing = item
            bid_created.bid = bid_made
            bid_created.save()
            item.start_bid = bid_made
            item.save()
            competitor = request.user.username
            item.winner = competitor
            item.save()
            return HttpResponseRedirect(reverse('listing', args=(item.id, )))
        else:
            competitor = item.winner
            return render(request, 'auctions/error.html')

@login_required
def saveWatchlist(request, listing_id):
    if request.method == 'POST':
        itemCurrent = AuctionListing.objects.get(pk=listing_id)
        watchlist, created = WatchList.objects.get_or_create(user=request.user)

        if itemCurrent in watchlist.own_list.all():
            watchlist.own_list.remove(itemCurrent)
        else: 
            watchlist.user=request.user
            watchlist.own_list.add(itemCurrent) ##watchlists

    return HttpResponseRedirect(reverse('listing', args=(itemCurrent.id, )))

@login_required
def close(request, listing_id):
    item = AuctionListing.objects.get(pk=listing_id)
    if request.user.username == item.owner and request.method == 'POST':
        item.active = False
        item.save()
        return HttpResponseRedirect(reverse('listing', args=(item.id,)))
    else:
        return HttpResponseRedirect(reverse('listing', args=(item.id, )))
    
@login_required
def comment(request, listing_id):
    item = AuctionListing.objects.get(pk=listing_id)
    if request.method == 'POST':
        form = CommentListing(request.POST)
        if form.is_valid():
            new_comment = Comment(
                comment = form.cleaned_data['comment_current'],
                product = item,
                user = request.user        
                )
    '''comment_sent = request.POST['comment_current']
    comentario = Comment(comment_sent, item.id, request.user.id)
    comentario.comment = comment_sent
    comentario.product = item
    comentario.user = request.user'''
    new_comment.save()
    return HttpResponseRedirect(reverse('listing', args=(item.id, )))