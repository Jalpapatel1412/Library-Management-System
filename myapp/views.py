from random import randint

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django import forms
from .tokens import account_activation_token
from datetime import datetime
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import Publisher, Book, Member, Order, Review
from .forms import SearchForm, OrderForm, ReviewForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.

class IndexView(View): #Optional feature : 04
    def get(self, request):
        if 'last_login' in request.session:
            last_login = request.session['last_login']
        else:
            last_login = "Last Login: more than one hour ago!!"
        username = request.user.username
        booklist = Book.objects.all().order_by('id')[:10]
        return render(request, 'myapp/index.html', {'booklist': booklist, 'username':username, 'last_login':last_login})

def about(request):
    response = HttpResponse()
    if 'number' in request.COOKIES:
        mynum = request.COOKIES['number']
    else:
        mynum = randint(1, 100)
        response.set_cookie('number', mynum, 30)
    lucky_number = render_to_string('myapp/about.html', {'mynum': mynum})
    response.write(lucky_number)
    return response

class DetailView(View): #Optional feature : 04
    def get(self, request, book_id):
        book_Detail = get_object_or_404(Book, id=book_id)
        return render(request, 'myapp/detail.html', {'book_title': book_Detail.title.upper(), 'book_price': book_Detail.price, 'book_publisher':book_Detail.publisher, 'book_id': book_id})

def findbooks(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            categoryName =''
            name = form.cleaned_data['your_name']
            category = form.cleaned_data['Select_category']
            max_price = form.cleaned_data['Maximum_Price']
            booklist = Book.objects.filter(price__lte=max_price)
            if category:
                booklist = booklist.filter(category=category)
                categoryName = dict(form.fields['Select_category'].choices)[category]
            return render(request, 'myapp/results.html', {'booklist':booklist, 'name':name, 'category':categoryName})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findbooks.html', {'form':form})

@login_required(login_url= '/myapp/login', redirect_field_name=None) #Optional feature : 08
def place_order(request): #Optional feature : 09
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            books = form.cleaned_data['books']
            order = form.save(commit=False)
            try:
                if Member.objects.get(id=request.user.id):  # Option feature: 08
                    memberObject = Member.objects.get(pk=request.user.id)
                    order.member= memberObject
                    order.save()
                    form._save_m2m()
                    if type == 1:
                        for b in order.books.all():
                            memberObject.borrowed_books.add(b)
                    return render(request, 'myapp/order_response.html', {'books': books, 'order':order})
                else:
                    return render(request, 'myapp/placeorder.html', {'form':form})
            except Member.DoesNotExist:
                # Member_err = "You are not a registered client"
                return HttpResponse('Your account not logged In')
    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form':form})

@login_required(login_url= '/myapp/login', redirect_field_name=None) #Optional feature : 08
def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            book = form.cleaned_data['book']
            reviewer = form.cleaned_data['reviewer']
            rating = form.cleaned_data['rating']
            comments = form.cleaned_data['comments']
            try:
                if Member.objects.get(id=request.user.id):  # Option feature: 08
                    memberObject = Member.objects.get(pk=request.user.id)
                    if memberObject.status != 3:
                        if 1 <= rating <= 5:
                            review.save()
                            book.num_reviews = book.num_reviews + 1
                            book.save(update_fields=['num_reviews'])
                            return redirect('myapp:index')
                        else:
                            return render(request, 'myapp/review.html',
                                          {'form': form, 'error': 'You must enter a rating between 1 and 5!'})
                    else:
                        return render(request, 'myapp/review.html',
                                  {'form': form, 'error': 'Guest Member can not submit a review'})
            except Member.DoesNotExist:
                # Member_err = "You are not a registered client"
                return HttpResponse('Your account not logged In')

    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form':form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        current_login_time = datetime.now()
        timestamp = current_login_time.strftime("%d-%b-%Y (%H:%M:%S)")
        request.session['last_login'] = 'Last Login: ' + timestamp
        request.session.set_expiry(3600)
        if user:
            if user.is_active:
                login(request, user)
                if request.session.get('bookid'):
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '')) #required feature : 04 Go back to chk_reviews
                else:
                    return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))

def chk_reviews(request, book_id):
    request.session['bookid'] = book_id #required feature : 4
    try:
        if Member.objects.get(id=request.user.id):
            book = get_object_or_404(Book, id=book_id)
            total = 0
            avg_review = 0
            ratings = Review.objects.filter(book__id=book_id)
            if ratings:
                for r in ratings:
                    rate = r.rating
                    total += rate
                total_no_of_reviews = Book.objects.get(id=book_id).num_reviews
                avg_review = int(total/total_no_of_reviews)
                del request.session['bookid'] #required feature : 04
                return render(request, 'myapp/chk_reviews.html', {'book': book, 'avg_review': avg_review})
            else:
                Rating_err = "There are no reviews as of now"
                return render(request, 'myapp/chk_reviews.html', {'book': book, 'Rating_Err': Rating_err })
        # else:
        #     return HttpResponse("You are not a registered Client")
    except Member.DoesNotExist:
        return render(request, 'myapp/login.html') #Go for the login page

@login_required(login_url= '/myapp/login', redirect_field_name=None) #Optional feature : 09
def myorders(request): #Optional feature : 09
    try:
        if Member.objects.get(id=request.user.id):
            orders = Order.objects.filter(member__id=request.user.id)
            return render(request, 'myapp/myorder.html', {'member_orders': orders})
        # else:
        #     return HttpResponse("You are not a registered Client")
    except Member.DoesNotExist:
        return HttpResponse("You are not a registered Client")

def user_signup(request): # Required feature : 03
    if request.method == 'POST':

        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('myapp/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message) # Extra feature : 10
            return redirect('myapp:account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'myapp/signup.html', {'form': form})

def account_activation_sent(request): # Extra feature : 10
    return render(request, 'myapp/account_activation_sent.html')

def activate(request, uidb64, token): # Extra feature : 10
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Member.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Member.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        # user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('myapp:index')
    else:
        return render(request, 'myapp/account_activation_invalid.html')