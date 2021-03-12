from django import forms

PAYMENT_CHOICES = {
    ('L','Paiement cash á la livraison'),
    ('C','Paiement par la carte bancaire'),
    ('M','Retrait en magasin')
}

class CheckoutForm(forms.Form):
    firstname = forms.CharField(max_length=100,required=True)
    lastname = forms.CharField(max_length=100,required=True)
    apartment_adress = forms.CharField(max_length=250)
    city = forms.CharField(max_length=100,required=True)
    zip = forms.CharField()
    phone = forms.CharField(max_length=10,required=True)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect,choices=PAYMENT_CHOICES)
    
