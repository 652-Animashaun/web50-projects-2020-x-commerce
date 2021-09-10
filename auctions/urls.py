from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("listItem/<int:listing_id>", views.listItem, name="listItem"),
    path("doBid/<int:listing_id>", views.doBid, name="doBid"),
    path("writecomment/<int:listing_id>", views.writecomment, name="writecomment"),
    path("addWatchlist/<int:listing_id>", views.addWatchlist, name="addWatchlist"),
    path("myWatchlist", views.myWatchlist, name="myWatchlist"),
    path("myWatchlist/delWatchlist/<int:listing_id>", views.delWatchlist, name="delWatchlist"),
    path("closeBid/<int:listing_id>",views.closeBid, name="closeBid"),
    path("categories", views.categories, name='categories'),
    path("<str:category>", views.catIs, name="catIs"),
    path("myauctions/<int:vendor>", views.myListings, name="myListings")
]
