from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist" , views.watchlist , name="watchlist"),
    path("remove_watchlist" , views.remove_watchlist, name="remove_watchlist"),
    path("add_watchlist" , views.add_watchlist , name="add_watchlist"),
    path("place_bid" , views.place_bid , name="place_bid"),
    path("closed_list", views.closed_list, name="closed_list"),
    path("unactive_item", views.unactive_item , name="unactive_item"),
    path("comment" , views.comment , name="create_comment"),
    path("add_category" , views.add_category, name="add_category"),
    path("item/<str:item>" , views.get_item , name="get_item"),
    path("item/", views.handle_get_empty_item, name="handle_get_empty_item")
]
 