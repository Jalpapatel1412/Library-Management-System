from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone

#publisher model
class Publisher(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField()
    city = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, default='USA', blank=False)

    def __str__(self):
        return self.name
#book model
class Book(models.Model):
    CATEGORY_CHOICES = [
        ('S', 'Scinece&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='F')
    num_pages = models.PositiveIntegerField(default=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(1000)]) #Optional feature : 02
    publisher = models.ForeignKey(Publisher, related_name='books', on_delete=models.CASCADE)
    description = models.CharField(max_length=100, blank=True)
    num_reviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Member(User):
    STATUS_CHOICES = [
        (1, 'Regular member'),
        (2, 'Premium Member'),
        (3, 'Guest Member'),
    ]

    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    address = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, default='ON')
    last_renewal = models.DateField(default=timezone.now)
    auto_renew = models.BooleanField(default=True)
    borrowed_books = models.ManyToManyField(Book, blank=True)
    image = models.ImageField(upload_to='profile_image', blank=False) #Option feature : 03

    def get_borrowed_books(self): #Optional feature : 06
        return ",".join([str(p) for p in self.borrowed_books.all()])

    def __str__(self):
        return self.first_name

class Order(models.Model):
    ORDER_CHOICES = [
        (0, 'Purchase'),
        (1, 'Borrow'),
    ]

    books = models.ManyToManyField(Book, blank=True)
    member = models.ForeignKey(Member, related_name="member", on_delete=models.CASCADE)
    order_type = models.IntegerField(choices=ORDER_CHOICES, default=1)
    order_Date = models.DateField(default=timezone.now)

    def total_items(self):
        total_items=str(self.books.count())
        return total_items

class Review(models.Model):
    reviewer = models.EmailField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.comments
