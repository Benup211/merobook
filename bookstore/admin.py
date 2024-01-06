from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Cart)
admin.site.register(Comment)
admin.site.register(EmailTokenGeneration)
admin.site.register(Wishlist)
admin.site.register(CartHistory)