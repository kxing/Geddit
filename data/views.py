# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from data.models import Category, Item, User
from data.forms import ItemForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from datetime import datetime
#from .auth import scripts_login

def index(request):
    return render(request, 'index.html', {
            'categories': Category.get_all_categories(),
            'items': Item.get_all_items(),
            'user': get_current_user(),
        },
        context_instance=RequestContext(request))

def create_listing(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            price = form.cleaned_data['price']
            
            active = True
            upload_time = datetime.utcnow
            
            # TODO: Grab username from web cert
            user = get_current_user()
            
            Item.create_item(user, name, description, category, price)
            print 'success'
            return redirect('data.views.index')
    else:
        return redirect('data.views.sell_page')

def sell_page(request):
    form = ItemForm()
        
    return render(request, 'create_listing.html', {
            'form': form,
            'categories': Category.get_all_categories(),
            'user': get_current_user(),
        },
        context_instance=RequestContext(request))

def get_current_user():
    # TODO: replace this with the user from the web cert
    return User.get_user('kxing')
