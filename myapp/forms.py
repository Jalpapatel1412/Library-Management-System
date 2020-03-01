from django import forms
from myapp.models import Order, Review, Member

class SearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('S', 'Scinece&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
    your_name = forms.CharField(max_length=100, required=False)
    Maximum_Price = forms.DecimalField(min_value=1, required=True)
    Select_category = forms.ChoiceField(widget=forms.RadioSelect,
                                        choices = CATEGORY_CHOICES,  required=False)
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['books', 'order_type']
        widgets = {'books': forms.CheckboxSelectMultiple(), 'order_type':forms.RadioSelect}
        # labels = {'member': u'Member name', }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'book', 'rating', 'comments']
        widgets = {'book': forms.RadioSelect()}
        labels = {'reviewer': u'Please enter a valid email', 'rating' : u'Rating: An integer between 1 (worst) and 5 (best)' }

class SignUpForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['username','first_name','last_name','status','address','city','province','email','password']
