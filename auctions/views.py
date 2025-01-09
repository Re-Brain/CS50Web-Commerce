from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from decimal import Decimal

############ User ############


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

############ Listing Pages #############


def findHighestBid(title):
    # Filter by the given title
    prices = Price.objects.filter(item__title=title)
    result = Decimal('0.00')  # Initialize the result as a Decimal

    for price in prices:
        if price.price > result:
            result = price.price  # Store the price.price value, not the Price object

    return result


def get_items(is_active, category):
    if category != "None":
        if is_active:
            return Item.objects.filter(is_active=True, category=category)
        else:
            return Item.objects.filter(is_active=False, category=category)
    else:
        if is_active:
            return Item.objects.filter(is_active=True)
        else:
            return Item.objects.filter(is_active=False)


def create_list(request, active):
    if request.method == "POST":
        category = request.POST["category"]
        selected = None

        if category == "None":
            items = get_items(active, "None")
        else:
            category = Categorie.objects.get(category=category)
            items = get_items(active, category)
            selected = category

        categories = Categorie.objects.all()
        lists = []
        for item in items:
            object = item
            highest_bid = findHighestBid(object)
            lists.append([object, highest_bid])

        return render(request, "auctions/index.html", {"lists": lists, "choices": categories, "selected": selected, "active": active})

    items = get_items(active, "None")
    categories = Categorie.objects.all()
    lists = []

    for item in items:
        object = item
        highest_bid = findHighestBid(object)
        lists.append([object, highest_bid])

    return render(request, "auctions/index.html", {"lists": lists, "choices": categories, "selected": None, "active": active})


def index(request):
    return create_list(request, True)


def closed_list(request):
    return create_list(request, False)

############ Create Auction #############


@login_required
def create(request):
    if request.method == "POST":
        item = Item.objects.create(
            user=request.user, description=request.POST["description"], image=request.POST["image"], title=request.POST["title"])

        category = Categorie.objects.get(category=request.POST["category"])

        item.category = category
        item.save()

        Price.objects.create(user=request.user, item=item,
                             price=request.POST["price"])

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html", {"choices": Categorie.objects.all()})


def add_category(request):
    if request.method == "POST":
        category = request.POST["new_category"]
        Categorie.objects.create(category=category)
        return HttpResponseRedirect(reverse("create"))

    return HttpResponseRedirect(reverse("create"))

############ Item Display #############
def get_item(request, item):

    list = Item.objects.get(title=item)
    bids = Price.objects.filter(item__title=item).count()
    price = findHighestBid(item)
    highest_bidder = Price.objects.get(price=price, item__title=item)
    comments = Comment.objects.filter(item=list)
    active = list.is_active
    user_bid = None
    user_watchlist = None

    if request.user.is_authenticated:
        user_bid = Price.objects.filter(
            item=list, price=price, user=request.user).exists()
        user_watchlist = Watchlist.objects.filter(user=request.user, item=list)

    return render(request, "auctions/item.html", {"item": list,
                                                  "bids": bids, "price": price,
                                                  "user_bid": user_bid, "user": request.user,
                                                  "user_watchlist": user_watchlist,
                                                  "highest_bidder": highest_bidder,
                                                  "active": active,
                                                  "comments": comments})

def handle_get_empty_item(request):
    return HttpResponseRedirect(reverse("index"))

@login_required
def place_bid(request):
    if request.method == "POST":
        item = Item.objects.get(title=request.POST["item"])
        current_highest_price = findHighestBid(item.title)
        bid_price = Decimal(request.POST["bid"])
        if bid_price >= current_highest_price:
            Price.objects.create(user=request.user, item=item, price=bid_price)
            return HttpResponseRedirect(reverse("get_item", args=(item.title,)))
        else:
            messages.error(request, "Your bet is too low. Please bet higher")
            return HttpResponseRedirect(reverse("get_item", args=(item.title,)))

    item = Item.objects.get(title=request.GET["item"])
    return HttpResponseRedirect(reverse("get_item", args=(item.title,)))


def unactive_item(request):
    if request.method == "POST":
        item = Item.objects.get(title=request.POST["item"])
        Watchlist.objects.filter(item=item).delete()
        item.is_active = False
        item.save()
        return HttpResponseRedirect(reverse("index"))

    return HttpResponseRedirect(reverse("index"))


@login_required
def comment(request):
    if request.method == "POST":
        item = Item.objects.get(title=request.POST["item"])
        comment = request.POST["comment"]
        user = request.user

        Comment.objects.create(item=item, comment=comment, user=user)
        return HttpResponseRedirect(reverse("get_item", args=(item.title,)))

    item = Item.objects.get(title=request.GET["item"])
    return HttpResponseRedirect(reverse("get_item", args=(item.title,)))

############ Watchlist #############

@login_required
def add_watchlist(request):
    if request.method == "POST":
        item = Item.objects.get(title=request.POST["item"])
        Watchlist.objects.create(item=item, user=request.user)
        return HttpResponseRedirect(reverse("get_item", args=(item.title,)))

    item = Item.objects.get(title=request.GET["item"])
    return HttpResponseRedirect(reverse("get_item", args=(item.title,)))


@login_required
def remove_watchlist(request):
    if request.method == "POST":
        item = Item.objects.get(title=request.POST["item"])
        Watchlist.objects.get(item=item, user=request.user).delete()
        return HttpResponseRedirect(reverse("get_item", args=(item.title,)))

    item = Item.objects.get(title=request.GET["item"])
    return HttpResponseRedirect(reverse("get_item", args=(item.title,)))


@login_required
def watchlist(request):
    watchlists = Watchlist.objects.filter(user=request.user)
    lists = []

    for watchlist in watchlists:
        item = watchlist.item
        highest_bid = findHighestBid(item)
        lists.append([item, highest_bid])

    return render(request, "auctions/watchlist.html", {"lists": lists})
