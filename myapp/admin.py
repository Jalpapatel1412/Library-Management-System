from django.contrib import admin
from  .models import Publisher, Book, Member, Order, Review

def add_price(modeladmin, request, queryset): #required feature : 02
    for book in queryset:
        book.price = book.price + 10
        book.save()
add_price.result = '$10 Price Added'

class BookAdmin(admin.ModelAdmin):
    fields = (('title', 'category', 'publisher'),('num_pages', 'price', 'num_reviews'))
    list_display = ('title', 'category', 'price')
    actions = [add_price, ] #required feature : 02

class OrderAdmin(admin.ModelAdmin):
    fields = ('books', ('member', 'order_type', 'order_Date'))
    list_display = ('id', 'member', 'order_type', 'order_Date', 'total_items')

class PublisherAdmin(admin.ModelAdmin):  #required feature : 01
    list_display = ('name','website','city')

class MemberAdmin(admin.ModelAdmin): #Optional feature : 06
    list_display = ('first_name', 'last_name', 'status', 'get_borrowed_books') #Optional feature : 06

# Register your models here.
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review)