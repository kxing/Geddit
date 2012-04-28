# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from data.models import Category, Item, User, Reservation
from data.forms import ItemForm, UserSettingsForm, ReservationForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from site_specific_functions import get_current_user
from django.contrib.auth.decorators import login_required

from data.views_lib import base_params

from datetime import datetime

NAV_PAGE = 'nav_page'
BUY = 'buy'
SELL = 'sell'
DASHBOARD = 'dashboard'
SETTINGS = 'settings'

def buy_page(request):
    render_params = base_params(request)
    render_params[NAV_PAGE] = BUY

    category = None
    if 'category' in request.GET:
        category = Category.get_category(request.GET['category'])

    search_query = request.GET.get('search_query', None)
    id = request.GET.get('id', None)

    render_params['items'] = Item.get_filtered_items(category, search_query, id)

    return render(request, 'buy.html', render_params, \
            context_instance=RequestContext(request))

def sell_page(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            price = form.cleaned_data['price']

            image = form.files.get('image', None)
            
            active = True
            upload_time = datetime.utcnow
            
            # TODO: Grab username from web cert
            get_current_user(request).add_item(name, description, category, price, image)
            return redirect('data.views.buy_page')
    else:
        # Create unbound form
        form = ItemForm()
    
    render_params = base_params(request)
    render_params[NAV_PAGE] = SELL
    render_params['form'] = form
    # For the Google Maps location
    if get_current_user(request).location is not None:
        render_params['latitude'] = get_current_user(request).location.latitude
        render_params['longitude'] = get_current_user(request).location.longitude
    render_params['items'] = get_current_user(request).get_items()
    
    return render(request, 'sell.html', render_params, \
                  context_instance=RequestContext(request))

def dashboard_page(request, message=None):
    render_params = base_params(request)
    render_params[NAV_PAGE] = DASHBOARD

    form = ReservationForm()
    render_params['form'] = form
    render_params['reservations'] = get_current_user(request).get_reservations()
    render_params['claims'] = get_current_user(request).get_claims()
    render_params['items'] = get_current_user(request).get_items()
    render_params['message'] = message
    return render(request, 'dashboard.html', render_params, \
            context_instance=RequestContext(request))

def remove_item(request):
    if request.method != 'POST':
        return redirect('data.views.sell_page')
    item = Item.get_item_by_id(request.POST['item_id'])
    get_current_user(request).remove_item(item)
    return redirect('data.views.sell_page')

def claim_listing(request):
    if request.method != 'POST':
        return redirect('data.views.buy_page')
    item = Item.get_item_by_id(request.POST['item_id'])
    get_current_user(request).add_claim(item)

    buyer = get_current_user(request)
    item = Item.get_item_by_id(request.POST['item_id'])
    item.seller_user.send_email(str(buyer) + ' wants to buy your ' + str(item) + '. Please contact your buyer at ' + buyer.email, '[Geddit] Buyer for ' + str(item))
    return redirect('data.views.dashboard_page', message='Item claimed, seller contacted')

def unclaim_listing(request):
    if request.method != 'POST':
        return redirect('data.views.dashboard_page')
    item = Item.get_item_by_id(request.POST['item_id'])
    get_current_user(request).remove_claim(item)
    return redirect('data.views.dashboard_page')

def make_reservation(request):
    if request.method != 'POST':
        return redirect('data.views.dashboard_page')
    form = ReservationForm(request.POST)
    if not form.is_valid():
        return redirect('data.views.dashboard_page')

    search_query = form.cleaned_data['search_query']
    max_price = form.cleaned_data['max_price']

    get_current_user(request).add_reservation(search_query, max_price)
    return redirect('data.views.dashboard_page')

def delete_reservation(request):
    if request.method != 'POST':
        return redirect('data.views.dashboard_page')

    reservation_id = request.POST['reservation_id']
    reservation = Reservation.get_reservation_by_id(reservation_id)
    get_current_user(request).remove_reservation(reservation)
    return redirect('data.views.dashboard_page')

def settings_page(request):
    if request.method == "POST":
        form = UserSettingsForm(request.POST, instance=get_current_user(request))
    
        if form.is_valid():
            form.save()
            return redirect('data.views.settings_page')
    else:
        # Create unbound form if GET
        initialData = {
            'cell_phone': get_current_user(request).cell_phone,
            'location': get_current_user(request).location
        }
        form = UserSettingsForm(initial=initialData)
    
    render_params = base_params(request)
    render_params[NAV_PAGE] = SETTINGS
    render_params['form'] = form
    
    return render(request, 'settings.html', render_params,
                  context_instance=RequestContext(request))

'''
def email_seller(request):
    if request.method != 'POST':
        return redirect('data.views.cart_page')
    print 'email sent'
    buyer = get_current_user(request)
    item = Item.get_item_by_id(request.POST['item_id'])
    item.seller_user.send_email(str(buyer) + ' wants to buy your ' + str(item) + '. Please contact your buyer at ' + buyer.email, '[Geddit] Buyer for ' + str(item))
    # TODO: show a confirmation message
    return redirect('data.views.cart_page')
'''

