from django.contrib import admin
from .models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "password" , "email")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("comment" , "user" , "item")
    
class PriceAdmin(admin.ModelAdmin):
    list_display = ("price" , "user" , "item")

class ItemAdmin(admin.ModelAdmin):
    list_display = ("title" , "image", "date" , "description", "category")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("item" , "user")

admin.site.register(User, UserAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Categorie)
admin.site.register(Watchlist, WatchlistAdmin)



