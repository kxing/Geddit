# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from data.models import Category, Item, User
from data.forms import ItemForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from datetime import datetime
#from .auth import scripts_login

def base_params():
    return { \
        'categories': Category.get_all_categories(), \
        'items': Item.get_all_items(), \
        'user': get_current_user(), \
    }

def buy_page(request):
    render_params = base_params()
    return render(request, 'buy.html', render_params, \
            context_instance=RequestContext(request))

def sell_page(request):
    form = ItemForm()
    render_params = base_params()
    render_params['form'] = form
    render_params['latitude'] = get_current_user().location.latitude
    render_params['longitude'] = get_current_user().location.longitude
        
    return render(request, 'create_listing.html', render_params, \
            context_instance=RequestContext(request))

def cart_page(request):
    render_params = base_params()
    render_params['claims'] = get_current_user().get_claims()
    return render(request, 'cart.html', render_params, \
            context_instance=RequestContext(request))

def create_listing(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            price = form.cleaned_data['price']
            image = form.files['image']
            
            active = True
            upload_time = datetime.utcnow
            
            # TODO: Grab username from web cert
            get_current_user().add_item(name, description, category, price, image)
            return redirect('data.views.buy_page')
    else:
        return redirect('data.views.sell_page')

def claim_listing(request):
    if request.method != 'POST':
        return redirect('data.views.buy_page')
    item = Item.get_item_by_id(request.POST['item_id'])
    get_current_user().add_claim(item)
    return redirect('data.views.cart_page')

def unclaim_listing(request):
    if request.method != 'POST':
        return redirect('data.views.cart_page')
    item = Item.get_item_by_id(request.POST['item_id'])
    get_current_user().remove_claim(item)
    return redirect('data.views.cart_page')

def email_seller(request):
    if request.method != 'POST':
        return redirect('data.views.cart_page')
    print 'email sent'
    buyer = get_current_user()
    item = Item.get_item_by_id(request.POST['item_id'])
    item.seller_user.send_email(str(buyer) + ' wants to buy your ' + str(item) + '. Please contact your buyer at ' + buyer.email, '[Geddit] Buyer for ' + str(item))
    # TODO: show a confirmation message
    return redirect('data.views.cart_page')

def get_current_user():
    # TODO: replace this with the user from the web cert
    return User.get_user('kxing')
