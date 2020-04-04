# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .form import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilters
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .decorator import unauthurizedUser, allowed_users, admin_only


# Create your views here.

# unauthorizedUser is a custom decorator
@unauthurizedUser
def register(request):
    form = CreateUserForm
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            mUser = form.save()

            # the new user will automatically assign to customer group
            group = Group.objects.get(name='customers')
            mUser.groups.add(group)

            # this will add a user to customer....
            Customer.objects.create(
                user=mUser,
                name=mUser.username,
            )

            c_user = form.cleaned_data.get('username')
            messages.success(request, 'Successfully created ...' + c_user)
            return redirect('/login')

    context = {'form': form}
    return render(request, 'polls/register.html', context)


@unauthurizedUser
def loginPage(request):
    if request.method == 'POST':
        # 'username && password '  it's a name in input field ..
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Something is wrong... ? ')

    context = {}
    return render(request, 'polls/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


# [customers] it's a group name
@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def userPage(request):
    order = request.user.customer.order_set.all()
    total_orders = order.count()
    delivered = order.filter(status='delivered').count()
    pending = order.filter(status='status').count()

    context = {'order': order,
               'total_orders': total_orders,
               'delivered': delivered,
               'pending': pending,
               }
    return render(request, 'polls/user.html', context)


@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    delivered = orders.filter(status='delivered').count()
    pending = orders.filter(status='pending').count()

    context = {'customers': customers,
               'orders': orders,
               'total_orders': total_orders,
               'delivered': delivered,
               'pending': pending}
    return render(request, 'polls/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    list1 = Product.objects.all()
    return render(request, 'polls/products.html', {'products': list1})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customers = Customer.objects.get(id=pk)
    order = customers.order_set.all()

    orderFilters = OrderFilters(request.GET, queryset=order)
    order = orderFilters.qs
    total_orders = order.count()

    context = {'customers': customers,
               'order': order,
               'total_orders': total_orders,
               'filters': orderFilters}

    return render(request, 'polls/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    # inlineformset_factory is method to create a multiple item's...
    orderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
    customer = Customer.objects.get(id=pk)
    # queryset to have no data on first view....
    formset = orderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = orderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/customer/' + str(customer.id))

    context = {'formSet': formset}
    return render(request, 'polls/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    # OrderForm is the db fields of Orders..
    # instance is the current order ..
    print('order', order)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'formSet': form}
    return render(request, 'polls/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'polls/delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def setting(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'polls/setting.html', context)
