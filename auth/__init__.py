import subprocess
import ldap
import ldap.filter

from django.contrib.auth.middleware import RemoteUserMiddleware
from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.views import login
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
import settings

def zephyr(msg, clas='message', instance='log', rcpt='nobody',):
    proc = subprocess.Popen(
        ['zwrite', '-d', '-n', '-c', clas, '-i', instance, rcpt, ],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
    proc.communicate(msg)

class ScriptsRemoteUserMiddleware(RemoteUserMiddleware):
    header = 'SSL_CLIENT_S_DN_Email'

class ScriptsRemoteUserBackend(RemoteUserBackend):
    def clean_username(self, username, ):
        if '@' in username:
            name, domain = username.split('@')
            assert domain.upper() == 'MIT.EDU'
            return name
        else:
            return username
    def configure_user(self, user, ):
        username = user.username
        user.password = "ScriptsSSLAuth"
        con = ldap.open('ldap-too.mit.edu')
        con.simple_bind_s("", "")
        dn = "dc=mit,dc=edu"
        fields = ['cn', 'sn', 'givenName', 'mail', ]
        userfilter = ldap.filter.filter_format('uid=%s', [username])
        result = con.search_s('dc=mit,dc=edu', ldap.SCOPE_SUBTREE, userfilter, fields)
        if len(result) == 1:
            user.first_name = result[0][1]['givenName'][0]
            user.last_name = result[0][1]['sn'][0]
            user.email = result[0][1]['mail'][0]
            try:
                user.groups.add(auth.models.Group.objects.get(name='mit'))
            except ObjectDoesNotExist:
                print "Failed to retrieve mit group"
        else:
            raise ValueError, ("Could not find user with username '%s' (filter '%s')"%(username, userfilter))
        try:
            user.groups.add(auth.models.Group.objects.get(name='autocreated'))
        except ObjectDoesNotExist:
            print "Failed to retrieve autocreated group"
        user.save()
        return user

def scripts_login(request, **kwargs):
    host = request.META['HTTP_HOST'].split(':')[0]
    if host == 'localhost':
        return login(request, **kwargs)
    elif request.META['SERVER_PORT'] == '444':
        if request.user.is_authenticated():
            # They're already authenticated --- go ahead and redirect
            if 'redirect_field_name' in kwargs:
                redirect_field_name = kwargs['redirect_field_names']
            else:
                from django.contrib.auth import REDIRECT_FIELD_NAME
                redirect_field_name = REDIRECT_FIELD_NAME
            redirect_to = request.REQUEST.get(redirect_field_name, '')
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            return HttpResponseRedirect(redirect_to)
        else:
            return login(request, **kwargs)
    else:
        # Move to port 444
        redirect_to = "https://%s:444%s" % (host, request.META['REQUEST_URI'], )
        return HttpResponseRedirect(redirect_to)
