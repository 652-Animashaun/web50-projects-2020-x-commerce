from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django import forms 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *

class newListing(forms.Form):
    title = forms.CharField(label="Title", max_length=64)
    description= forms.CharField(label="Description", max_length=200)
    imageUrl= forms.URLField()
    initialBid=forms.IntegerField()
    category= forms.CharField(label="Category", max_length=36)

class makeBid(forms.Form):
    bid= forms.IntegerField(label="Place Bid")

class newComment(forms.Form):
    comment= forms.CharField(label="comment", max_length=200)
    

def index(request):

    return render(request, "auctions/index.html",{
        "activelistings": Listing.objects.filter(is_active=True),
        })
def createListing(request):

    if request.method == "POST":
        form = newListing(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description= form.cleaned_data['description']
            initialBid= form.cleaned_data['initialBid']
            imageUrl= form.cleaned_data['imageUrl']
            category= form.cleaned_data['category']
            
            if request.user.is_authenticated:
                vendor= request.user

                listing = Listing(title=title, description=description, imageUrl=imageUrl, initialBid=initialBid, vendor=vendor, category=category)
                listing.save()
                return render(request, "auctions/index.html",{
                    "activelistings":Listing.objects.all()
                    })
            else:
                return render(request, "auctions/createlisting.html",{
                    "form":newListing(),
                    "message": "Please loging to list an item"
                    })
        else:
            return render(request, "auctions/createlisting.html",{
            "form": newListing(),
            "message": "all form inputs are required"
            })
    else:
        return render(request, "auctions/createlisting.html",{
            "form": newListing()
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

def listItem(request, listing_id):
    Item = Listing.objects.get(id=listing_id)
    if Item is not None and Item.is_active is True:
        return render(request, "auctions/itempage.html",{
            "Item":Item,
            "form":newComment(),
            "comments": Comments.objects.filter(listingId=Item),
            "bidform":makeBid()
            })
    elif Item.is_active is True and Item.vendor.id == request.user.id:
        pass

    elif Item.is_active is False and Item.vendor.id == request.user.id:
        return render(request, "auctions/itempage.html",{
            "Item":Item,
            "message":"You've closed this bid!",
            "comments": Comments.objects.filter(listingId=Item)
            })
    elif Item.is_active is False and Item.highestBidder.bidder.id == request.user.id:
        return render(request, "auctions/sold.html",{
            "message": "Sold! You won the bid! Lets grab a beer soon.",
            "Item":Item
            })
    elif Item.is_active is False and Item.highestBidder.id != request.user.id:
        return render(request, "auctions/sold.html",{
            "message": "Bid Closed. Sold to the highestBidder"
            })



def doBid(request, listing_id):
    Item = Listing.objects.get(id=listing_id)
    
    if request.method=="POST":
        if request.user.is_authenticated:
            user= request.user
            form = makeBid(request.POST)
            if form.is_valid():
                bid= form.cleaned_data['bid']
                if Item.highestBid is None:
                    Item.highestBid = int(0)
                if Item.highestBid < bid and Item.initialBid < bid:

                    currBid = Bid(listingId=Item, currBid=bid, bidder=user)
                        
                    Item.highestBid= bid
                    Item.highestBidder= currBid
                    currBid.save()
                    Item.save()
                    return HttpResponseRedirect(reverse("listItem", kwargs={'listing_id':Item.id}))
                elif Item.highestBid >= bid or Item.initialBid >= bid:
                    return render(request, "auctions/itempage.html",{
                        "message": "You need to beat the starting or highest bid",
                        "Item":Item,
                        "bidform":makeBid()
                                                })
        else:
            return render(request, "auctions/login.html",{
                "message": "Hommie, login to bid"
                })
    else:
        return render(request, "auctions/itempage.html",{
            "Item":Item,
            "bidform":makeBid()
            })

def writecomment(request, listing_id):

    Item= Listing.objects.get(id=listing_id)

    if request.method=="POST":
        if request.user.is_authenticated:
            user = request.user
            form = newComment(request.POST)
            if form.is_valid():
                comment= form.cleaned_data['comment']
                newcom= Comments(userId=user, comment=comment, listingId=Item)
                newcom.save()
                
                
                return HttpResponseRedirect (reverse("listItem", kwargs={'listing_id':Item.id}))
        else:

            return render(request, "auctions/login.html", {
                "message": "Sorry we had to bring you back here. Please login"
                })
    else:
        return render(request, "auctions/itempage.html", {
            "form":newComment(),
            "Item":Item,
            "comments": Item.Comments
            })

def addWatchlist(request, listing_id):
    Item = Listing.objects.get(id=listing_id)
    print(request.user)
    if request.user.is_authenticated:
        user = request.user
        
        # Need to check if user already added item to watchlist, 
        added = Watchlist.objects.filter(listingId=Item, userId=user)
        userWatchlist = []
        for watchitem in added:
            listing = watchitem.listingId.id
            print(listing)
            userWatchlist.append(listing)
        watchlist= Watchlist.objects.filter(userId=user)
        if Item.id in userWatchlist:
            print(f"found {Item} in {user} watchlist")
            return render(request, "auctions/watchlist.html", {
                    "message": "You've already added this item to your watchlist!",
                    "Item":Item,
                    "watchlist":watchlist
                    })
        else:
            add = Watchlist(userId=user, listingId=Item)
            add.save()
            watchlist= Watchlist.objects.filter(userId=user)
            return render(request, "auctions/watchlist.html", {
                    "message": "Item added to your watchlist!",
                    "Item":Item,
                    "watchlist":watchlist
                    })

    else:
        return render(request, "auctions/login.html", {
                "message": "Sorry we had to bring you back here. Please login"
                })

def myWatchlist(request):
    if request.user.is_authenticated:
        user= request.user
        watchlist= Watchlist.objects.filter(userId=user)

        return render(request, "auctions/watchlist.html",{
            "watchlist":watchlist
            })

def catIs(request, category):


    items = Listing.objects.filter(category= category)
    return render(request, "auctions/catIs.html",{
        "activelistings": items
        })

def delWatchlist(request, listing_id):
    if request.user.is_authenticated:
        user = request.user
        Item = Watchlist.objects.filter(userId=user, listingId=listing_id)
        Item.delete()
        watchlist= Watchlist.objects.filter(userId=user)
        return render(request, "auctions/watchlist.html",{
            "watchlist":watchlist,
            "message": "Item removed!"
            })
    else:
        return render(request, "auctions/login.html",{
            "message":"Please login to perform operation"
            })
def closeBid(request, listing_id):
    Item = Listing.objects.get(id=listing_id)
    if Item.is_active is True and Item.vendor.id == request.user.id:
        Item.is_active=False
        Item.save()
        return render(request, "auctions/itempage.html", {
            "Item":Item,
            "message":"You've closed this bid!",
            "comments": Comments.objects.filter(listingId=Item)
            })
def categories(request):
    listing = Listing.objects.all()
    categories = []
    for item in listing:
        cat = item.category
        if cat not in categories:
            categories.append(cat)
    print(f"{categories}")
    return render(request, "auctions/categories.html", {
        "categories": categories
    })    

def myListings(request, vendor):
    vendor = vendor
    user = request.user.id 
    if user == vendor:
        mylist = Listing.objects.filter(vendor=vendor)

        return render(request, "auctions/mylisting.html", {
            "mylist":mylist
            })
    else:
        return render(request, "auctions/mylisting.html", {
            "message":"hmm, how did you get here? You can not view this page!"
            })
