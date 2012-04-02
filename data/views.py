# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from data.models import Category, Item

#from .auth import scripts_login

def index(request):
    t = loader.get_template('index.html')
    c = RequestContext(request, \
            {'categories': Category.get_all_categories(),
            'items' : Item.get_all_items()
            })
    return HttpResponse(t.render(c))
