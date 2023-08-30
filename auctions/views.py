from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, WatchList, AuctionListing

class Counter():
    def __init__(self, num):
        self.counter = num

    def add(self):
        self.counter += 1 
    
    def ver(self):
        return self.counter

class NewListing(forms.Form):
    title = forms.CharField(label='Titulo de la pagina')
    descrip = forms.CharField(max_length=120)
    bid = forms.IntegerField()
    image = forms.URLField()
    category = forms.CharField()

count = Counter(1)
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
        global count
        count.add()
        form = NewListing(request.POST)
        if form.is_valid():
            new_listing = AuctionListing(
                pk = count.ver(),
                title = form.cleaned_data['title'],
                description = form.cleaned_data['descrip'],
                start_bid = form.cleaned_data['bid'],
                image = form.cleaned_data['image'],
                category = form.cleaned_data['category']
            )

        ##watchlist = WatchList.objects.get(pk = int(request.POST['own_list']))
        ##watchlist.own_list.add(new_listing)
        return render(request, 'auctions/index.html',{
            'listings': AuctionListing.objects.all()
        })
    else:
        return render(request, 'auctions/create.html')