from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegistrationForm, LoginForm, ListingForm, addBidForm, CommentForm

from .models import Category, Listing, Bid, Comment

User = get_user_model()

def index(request):
    activeListing = Listing.objects.filter(isActive=True).order_by('-listed_at')
    watchlistCount = 0

    if request.user.is_authenticated:
        watchlistCount = request.user.watchlist.all().count()

    return render(request, "auctions/index.html", {
        "listings": activeListing, "watchlistCount": watchlistCount
    })
    
def categories(request):
    if request.method == "POST":
        categoryForm = request.POST['category']
        allCategories = Category.objects.all()
        watchlistCount = request.user.watchlist.all().count()

        activeListing = None
        if categoryForm == "No Category":
             # If "No Category" is selected, filter listings with no category
            activeListing = Listing.objects.filter(category__isnull=True)
        elif categoryForm:
            try:
                # If a specific category is selected, filter listings by that category
                category = Category.objects.get(categoryName=categoryForm)
                activeListing = Listing.objects.filter(isActive=True, category=category)
            except Category.DoesNotExist:
                # If the selected category does not exist, do nothing (show all active listings)
                pass
        
        return render(request, "auctions/categories.html", {
            "categories": allCategories, "listings": activeListing,
            "watchlistCount": watchlistCount
        })
    else:
        watchlistCount = request.user.watchlist.all().count()
        allCategories = Category.objects.all()
        activeListing = Listing.objects.filter(isActive=True).order_by('-listed_at')
        return render(request, "auctions/categories.html", {
            "categories": allCategories, "listings": activeListing,
            "watchlistCount": watchlistCount
        })

def listing(request, id):
    listing = Listing.objects.get(pk=id)
    listingWatchlist = request.user in listing.watchlist.all()
    owner = request.user.username == listing.owner.username

    countBid = Bid.objects.filter(listing=listing).count()
    watchlistCount = request.user.watchlist.all().count()

    # Find the current highest bid user
    highest_bid = Bid.objects.filter(listing=listing).order_by('-bid').first()
    highest_bid_user = highest_bid.user if highest_bid else None

    allComment = Comment.objects.filter(listing=listing).order_by('-created_at')

    # Retrieve and clear session message
    message = request.session.pop('message', None)
    updated = request.session.pop('updated', None)

    bidform = addBidForm()
    commentform = CommentForm()

    return render(request, "auctions/listing.html", {
        "listing": listing, "listingWatchlist": listingWatchlist,
        "owner": owner, "countBid": countBid,
        "highest_bid_user": highest_bid_user,
        "watchlist": watchlist, "allComment": allComment,
        "watchlistCount": watchlistCount, "bidform": bidform,
        "message": message, "updated": updated, "commentform": commentform
    })

def addBid(request, id):
    if request.method == "POST":
        form = addBidForm(request.POST)
        if form.is_valid():
            newBid = form.cleaned_data.get('bid')
            listing = Listing.objects.get(pk=id)
            if newBid > listing.price:
                updateBid = Bid(bid=newBid, user=request.user, listing=listing)
                updateBid.save()
                listing.price = newBid
                listing.save()

                request.session['message'] = "Bid updated successfully"
                request.session['updated'] = True
            else:
                # Message to display after redirection
                request.session['message'] = "Bid must be higher than the current price"
                request.session['updated'] = False
        else:
            request.session['message'] = "Invalid bid. Please enter a valid amount."
            request.session['updated'] = False

    return HttpResponseRedirect(reverse("listing", args=(id, )))
    
    
def closeAuction(request, id):
    listing = Listing.objects.get(pk=id)
    listing.isActive = False
    listing.save()

    request.session['message'] = "Auction was closed successfully"
    request.session['updated'] = True

    return HttpResponseRedirect(reverse("listing", args=(id, )))

def removeWatchlist(request, id):
    listing = Listing.objects.get(pk=id)
    currentUser = request.user
    listing.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def addWatchlist(request, id):
    listing = Listing.objects.get(pk=id)
    currentUser = request.user
    listing.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def watchlist(request):
    watchlist = request.user.watchlist.all().order_by('-listed_at')
    watchlistCount = watchlist.count()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist, "watchlistCount": watchlistCount
    })

def comment(request, id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            listing = Listing.objects.get(pk=id)
            comment = form.cleaned_data.get("message")
            currentUser = request.user

            newComment = Comment(author=currentUser, listing=listing, message=comment)
            newComment.save()

            request.session['message'] = "Comment added successfully"
            request.session['updated'] = True
        else:
            for error in form.errors['message']:
                request.session['message'] = error
                request.session['updated'] = False
                break

        return HttpResponseRedirect(reverse("listing", args=(id, )))


def create_list(request):
    if request.method == "GET":
        categorys = Category.objects.all()
        watchlistCount = request.user.watchlist.all().count()
        form = ListingForm()
        return render(request, "auctions/create.html", {
            "categorys": categorys, "watchlistCount": watchlistCount,
            "form": form
        })
    else:
        # Get the form data
        form = ListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            image = form.cleaned_data.get('imageUrl')
            price = form.cleaned_data.get('price')
            category = request.POST.get('category')

            # Current User
            currentUser = request.user

            # Get the particuar category
            categoryData = None
            if category:
                try:
                    # Get the particular category
                    categoryData = Category.objects.get(categoryName=category)
                except Category.DoesNotExist:
                    # If category does not exist, set categoryData to None and continue
                    categoryData = None

            # Create a new list object
            newList = Listing(title=title,
                            description=description,
                            imageUrl=image,
                            price=float(price),
                            owner=currentUser,
                            category=categoryData)

            # Insert newList into databse
            newList.save()

            # Create Bid object
            bid = Bid(listing=newList, user=currentUser, bid=price)
            bid.save()

            return HttpResponseRedirect(reverse(index))
        else:
            categorys = Category.objects.all()
            watchlistCount = request.user.watchlist.all().count()

            return render(request, "auctions/create.html", {
                'form': form, "categorys": categorys,
                "watchlistCount": watchlistCount
            })

        


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        # Attempt to sign user in
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "auctions/login.html", {
                    "form": form, "message": "Invalid username and/or password."
                })
    else:
        form = LoginForm()

    return render(request, "auctions/login.html", {
        'form': form
    })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Attempt to create new user
            user = User.objects.create_user(username, email, password)
            user.save()
            login(request, user)
            return redirect("index")
            
    else:
        form = RegistrationForm()
        
    return render(request, "auctions/register.html", {
        "form": form
    })
