# coding: utf-8
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import transaction, IntegrityError
from django.http import HttpResponseRedirect, Http404
from Substitute_Platform.models import Products, Categories, platform_user
from .forms import RegistrationForm, AuthenticationForm, ModificationForm



def index(request):
    """
    Index page
    """
    return render(request, 'Substitute_Platform/index.html')


def listing_substitutes(request):
    """
    Find 6 substitutes for a given product using nutritional score
    substitutes and substitutent have in common at least 1 category, up to 3
    """
    context = {}
    if request.method == 'GET':
        query = request.GET.get('query')
        query = " ".join(query.split())
        try:
            product_to_substitute = Products.objects.filter(
                name__icontains=query)[0]
        except IndexError:
            raise Http404()
        categories_p = []
        for elt in product_to_substitute.categories.all():
            categories_p.append(elt.id)

        substituents = Products.objects.filter(
            categories=categories_p[0]).filter(
                categories=categories_p[1]).filter(
                    categories=categories_p[2]).order_by(
                        'nutrition_grade').distinct()[:6]

        if len(substituents) < 6:
            substituents = Products.objects.filter(
                categories=categories_p[0]).filter(
                    categories=categories_p[1]).order_by(
                        'nutrition_grade').distinct()[:6]

        if len(substituents) < 6:
            substituents = Products.objects.filter(
                categories=categories_p[0]).order_by(
                    'nutrition_grade').distinct()[:6]

        context = {
            'substituted': product_to_substitute,
            'substituents': substituents,
        }

        return render(request, 'Substitute_Platform/substitutes_list.html',
                      context)
    else:
        with transaction.atomic():
            try:
                user = get_object_or_404(User, username=request.user)
                sbent_name = request.POST.get('checkbox')
                sbted_name = request.POST.get('substituted_name')
                substituent = Products.objects.filter(name=sbent_name)[0]
                substituted = Products.objects.filter(name=sbted_name)[0]
                plat_user = platform_user.objects.create(
                    user=user,
                    substituted_product=substituted,
                    substituent_product=substituent)
                plat_user.substituted_product_id = substituted.id
                plat_user.substituent_product.id = substituent.id
                query_v = request.POST.get('query_value')
            except IntegrityError:
                query_v = request.POST.get('query_value')
        return HttpResponseRedirect("")


def detail(request, product_id):
    """
    Give details about a product
    """
    product = get_object_or_404(Products, pk=product_id)
    context = {
        'product': product
    }
    return render(request, 'Substitute_Platform/details.html', context)


def account(request):
    """
    Give informations about user actually connected and gives possibility
    to change mail and password
    """

    if request.user.is_authenticated:
        user = User.objects.get(email=request.user.email)
        context = {
            'pseudo': user.username,
            'email': user.email,
            'request': request
        }
        if request.method == 'POST':
            form = ModificationForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']
                try:
                    with transaction.atomic():
                        print('password : {} email : {}'.format(password, email))
                        if len(password):
                            user.set_password(password)
                            user.save()
                            userConnect = authenticate(request,
                                                         username=user.username,
                                                         password=password)
                            login(request, user)
                        if len(email):
                            user.email = email
                            user.save()

                        return redirect('Substitute_Platform:account')
                except IntegrityError:
                    form.errors['internal'] = ("Erreur interne, "
                                               "merci de réitérer votre requête")
            else:
                context = {
                    'form': form
                }
                context['errors'] = form.errors.items()

    else:
        return redirect('Substitute_Platform:authentication')

    form = ModificationForm()
    context = {
        'form': form,
        'pseudo': user.username,
        'email': user.email,
        'request': request
    }

    return render(request, 'Substitute_Platform/account.html', context)


def registration(request):
    """
    Page to register
    """
    context = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            try:
                with transaction.atomic():
                    user = User.objects.create_user(username, email, password)
                    user = authenticate(request, username=username,
                                        password=password)
                    login(request, user)
                    return redirect('Substitute_Platform:account')
            except IntegrityError:
                form.errors['internal'] = ("Erreur interne, "
                                           "merci de réitérer votre requête")
        else:
            context = {
                'form': form
            }
            context['errors'] = form.errors.items()
            return render(request, 'Substitute_Platform/registration.html',
                          context)

    if request.user.is_authenticated:
        return redirect('Substitute_Platform:account')

    form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'Substitute_Platform/registration.html', context)


def connect(request):
    """
    Page to connect to an account
    """
    context = {}
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Substitute_Platform:account')

            context = {
                'form': form
            }
            context['errors'] = form.errors.items()
            return render(request, 'Substitute_Platform/connect.html',
                          context)
    else:
        if request.user.is_authenticated:
            return redirect('Substitute_Platform:account')

    form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'Substitute_Platform/connect.html', context)


def disconnect(request):
    """
    Disconnect you from your account (do nothing if you are not connected)
    """
    logout(request)
    return redirect('Substitute_Platform:index')


def my_substitutes(request):
    """
    List all your couples substitued/substituent products
    """
    if request.user.is_authenticated:
        user = User.objects.filter(username=request.user)[0]
        substitutes = platform_user.objects.filter(user=user).all()
        context = {
            'substitutes': substitutes
        }
    else:
        return redirect('Substitute_Platform:authentication')
    return render(request, 'Substitute_Platform/my_substitutes.html', context)


def legal_notice(request):
    """
    Display legal notice about the website
    """
    return render(request, 'Substitute_Platform/legal_notice.html')
