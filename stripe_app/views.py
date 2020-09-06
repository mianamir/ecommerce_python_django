from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
import json
import datetime

import stripe

stripe.api_key = "sk_test_51HMu04KMyUfoiWLNh2ACksVxeOQsxGy2m2MJfpNU7LeuwjnAhAsBcanvmrrRIBjivnQENCGadEObMSkKkuDWz9nr00SQw1OKvf"

from .models import *


def stripe_index(request):
    return render(request, "stripe_app_frontend/index.html")


def charge(request):

    amount = int(request.POST['amount'])
    
    if request.method == 'POST':
        print(f"Data: {request.POST}")

        customer = stripe.Customer.create(
            email = request.POST['email'],
            name = request.POST['nickname'],
            source = request.POST['stripeToken']
        )

        charge = stripe.Charge.create(
            customer = customer,
            amount = amount * 100,
            currency = 'usd',
            description = 'Donation'
        )
    
    return JsonResponse('Payment has been donated using Stripe.', safe=False)
    # return redirect(reverse('success', args=[amount]))
    # return redirect('stripe_success', args=[amount])


def success_message(request, args):
    amount = args
    return render(request, 'stripe_app_frontend/success.html', {'amount': amount})
