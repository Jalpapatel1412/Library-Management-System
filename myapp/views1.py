# Import necessary classes
from django.http import HttpResponse
from .models import Publisher, Book, Member, Order

# Create your views here.
def index(request):
    response = HttpResponse()
    booklist = Book.objects.all().order_by('pk')[:10]
    publisherlist = Publisher.objects.all().order_by('city')[:10]

    heading1 = '<b><p>' + 'List of available books: ' + '</b></p>'
    response.write(heading1)
    for book in booklist:
        para = '<p>'+ str(book.id) + ': ' + str(book) + '</p>'
        response.write(para)

    heading2 = '<b><p>' + 'List of available publishers: ' + '</b></p>'
    response.write(heading2)
    for publisher in publisherlist:
        para = '<p>'+ str(publisher.name) + ': ' + str(publisher.city) + '</p>'
        response.write(para)
    return response

def about(request):
     # response = HttpResponse()
    # heading1 = '<b><p>' + 'List of available books: ' + '</b></p>'
    # response.write(heading1)
    return HttpResponse('<b><h1>' + 'This is an eBook APP ' + '</b></h2>')

def detail(request, book_id):
    response = HttpResponse()

    try:
        bookdetail = Book.objects.get(id=book_id)

        bookheading = '<p>' + '<b> BookName </b>' + ' : ' + str(bookdetail.title.upper()) + '</p>'
        response.write(bookheading)

        priceheading = '<p>' + '<b> BookPrice </b>' + ' : ' + str(bookdetail.price) + '</p>'
        response.write(priceheading)

        publisherheading = '<p>' + '<b> BookPublisher </b>' + ' : ' + str(bookdetail.publisher) + '</p>'
        response.write(publisherheading)

    except Book.DoesNotExist:
        response.write("Book with this Id is not found")

    return response