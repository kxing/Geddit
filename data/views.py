# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.contrib.auth.views import login

#from .auth import scripts_login

def index(request):
    t = loader.get_template('index.html')
    c = Context()
    return HttpResponse(t.render(c))
